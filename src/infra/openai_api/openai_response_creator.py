from typing import Dict, Any, Type, TypeVar, AsyncIterator, Optional
from pydantic import BaseModel
from src.infra.openai_api.settings.openai_api_connection_handler import OpenAIAPIConnectionHandler

from src.config.logger_config import setup_logger
logger = setup_logger(name="OpenAIResponseCreator")

Model = TypeVar("Model", bound=BaseModel)


class OpenAIResponseCreator:
    async def create(self,
                     prompt_id: str,
                     variables: Dict[str, Any],
                     text_format: Type[Model],
                     max_output_tokens: int = 1600
                     ) -> Model:
        try:
            logger.info("Enviando requisição para API da OpenAI...")

            return await self.__create_structured_model_response(prompt_id, variables,
                                                                 max_output_tokens,
                                                                 text_format)

        except Exception as exception:
            logger.exception(f"Exceção ao obter resposta da API da OpenAI...")
            raise

    @classmethod
    async def __create_structured_model_response(cls, prompt_id: str, variables: Dict[str, Any],
                                                 max_output_tokens: int,
                                                 text_format: Type[Model]) -> Model:
        async with OpenAIAPIConnectionHandler() as openai:
            response = await openai.client.responses.parse(
                prompt={
                    "id": prompt_id,
                    "variables": variables
                },
                max_output_tokens=max_output_tokens,
                text_format=text_format)

            logger.info("Reposta da API da OpenAI obtida com sucesso!")

            if not response.output_parsed:
                raise IndexError(
                    'Não foi possível transformar a resposta da validação de query da OpenAI em um Pydantic Model.')

            return response.output_parsed
