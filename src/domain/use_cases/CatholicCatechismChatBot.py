import httpx
from pathlib import Path
from typing import Optional, Dict, Any, AsyncGenerator
from openai.types.responses import ResponseInputParam, ResponsePromptParam
from src.errors.types.server_error import ServerError
from src.domain.services.query_validator import QueryValidator
from src.infra.openai_api.openai_stream_response_creator import OpenAIStreamResponseCreator

from src.config.logger_config import setup_logger
logger = setup_logger(name="CatholicCatechismChatBot")


class CatholicCatechismChatBot:
    def __init__(self, prompt_id: str) -> None:
        self.prompt_id = prompt_id

        self.stream_response_creator = OpenAIStreamResponseCreator()
        self.previous_response_id: Optional[str] = self.stream_response_creator.last_response_id
        self.__catholic_catechism_api_url = "https://catholic-catechism-rag-api.aight.com.br/hybrid_search"
        self.__top_k = 3

    async def generate_assistant_response(self, user_message: str) -> AsyncGenerator[str, None] | str:
        logger.info("Gerando resposta do assistente...")
        self.previous_response_id = self.stream_response_creator.last_response_id

        if not self.previous_response_id:
            response = await self.__catholic_catechism_paragraphs_api_request(query=user_message)

            if response.status_code != 200:
                logger.info(
                    "Tratando a resposta mal-sucedida da API do Catecismo da Igreja Católica...")
                return self.__structure_output_for_unsuccessful_catechism_api_response(response=response)

            prompt = self.__structure_response_prompt(
                response=response, user_message=user_message)

            return self.stream_response_creator.create(prompt=prompt)

        query_validation = QueryValidator()

        try:
            if await query_validation.is_inappropriate_query(query=user_message):
                return f"""
                Este questionamento não é próprio para o contexto deste chatbot.
                Por favor, realize um questionamento válido e respeitoso!
                """
        except Exception:
            body = {
                'assistant_message': "Desculpe, aconteceu um error interno no servidor.\nPor favor, volte mais tarde!"}
            message = "Exceção ao avaliar se a query é própira/imprópria para o contexto da aplicação."
            raise ServerError(message=message, body=body)

        input_data = self.__structure_response_input(user_message)

        return self.stream_response_creator.create(input=input_data)

    async def __catholic_catechism_paragraphs_api_request(self, query: str) -> httpx.Response:
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
            try:
                logger.info(
                    f"Obtendo os {self.__top_k} parágrafos do Catecismo da Igreja Católica mais similares com query recebida...")

                response = await client.post(
                    self.__catholic_catechism_api_url,
                    json={"query": query, "top_k": self.__top_k}
                )

                logger.info(
                    "Resposta da API do Catecismo da Igreja Católica obtida com sucesso!")

                return response
            except Exception:
                body = {
                    'assistant_message': "Desculpe, aconteceu um error interno no servidor.\nPor favor, volte mais tarde!"}
                message = "Exceção ao obter resposta da API de Parágrafos do Catecismo."

                logger.exception(message)

                raise ServerError(message=message, body=body)

    @classmethod
    def __structure_output_for_unsuccessful_catechism_api_response(cls, response: httpx.Response) -> str:
        response_obj = response.json()

        # Erro por query confusa.
        if response.status_code == 406:
            return f"""
            Não foi possível entender completamente seu questionamento.
            Motivo: {response_obj['body']['query_validation']['reasons']}
            Por favor, melhore sua pergunta. Ok?!
            """

        # Erro de validação
        elif response.status_code == 400:
            return """
            Seu questionamento deve possuir no mínimo 8 e no máximo 808 caracteres.
            Por favor, melhore sua pergunta. Ok?!
            """

        # Erro de domínio: conteúdo indevido ou conteúdo fora do escopo
        elif response.status_code == 422:
            return f"""
            O questionamento realizado não tem relação de contexto para este Chatbot.
            Motivo: {response_obj['body']['error'][0]['query_validation']['reasons']}
            Por favor, faça uma nova pergunta!
            """

        # Erro no servidor
        else:
            body = {
                'warning_message': "Desculpe, aconteceu um error interno no servidor. Por favor, volte mais tarde!"}
            message = "Execeção na API de parágrafos do catecismo da Igreja Católica."
            raise ServerError(message=message, body=body)

    @classmethod
    def __structure_catechism_paragraphs_markdown(cls, body: Dict[str, Any]) -> str:
        paragraphs_markdown = ""
        for index, value in enumerate(body['points']):
            paragraphs_markdown += f""" 
            > {index + 1}º Parágrafo - {str(round(value['similarity_score'], 2))}% de Similaridade com Query:
                 - {str(value['text'])};
                 - Localização do Parágrafo:
                    {str(value['localization'])}
            """

        return paragraphs_markdown

    def __structure_response_prompt(self, response: httpx.Response, user_message: str) -> ResponsePromptParam:
        body = response.json()['body']
        catechism_paragraphs = self.__structure_catechism_paragraphs_markdown(
            body=body)

        prompt = ResponsePromptParam(
            id=self.prompt_id,
            variables={
                "query": user_message,
                "catechism_paragraphs": catechism_paragraphs
            }
        )

        return prompt

    @classmethod
    def __structure_response_input(cls, user_message: str):
        system_instruction = Path(
            "src/data/prompt/conversation_instruction.txt"
        ).read_text(encoding="utf-8")

        input_data: ResponseInputParam = [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": system_instruction}]
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": user_message}]
            }
        ]

        return input_data
