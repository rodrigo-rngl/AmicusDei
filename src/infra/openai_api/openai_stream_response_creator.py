from typing import AsyncGenerator, Optional
from openai.types.responses import ResponseInputParam, ResponsePromptParam
from src.infra.openai_api.settings.openai_api_connection_handler import OpenAIAPIConnectionHandler


from src.config.logger_config import setup_logger
logger = setup_logger(name="OpenAIStreamResponseCreator")


class OpenAIStreamResponseCreator:
    def __init__(self) -> None:
        self.last_response_id: Optional[str] = None

    async def create(self,
                     prompt: Optional[ResponsePromptParam] = None,
                     input: str | ResponseInputParam = [],
                     max_output_tokens: int = 4600) -> AsyncGenerator[str, None]:
        async with OpenAIAPIConnectionHandler() as openai:
            try:
                logger.info(
                    "Enviando requisição para API da OpenAI (stream)...")

                async with openai.client.responses.stream(
                    model="gpt-5-mini",
                    prompt=prompt,
                    input=input,
                    previous_response_id=self.last_response_id,
                    max_output_tokens=max_output_tokens
                ) as stream:
                    # Consome eventos do stream
                    async for event in stream:
                        # Texto incremental
                        if event.type == "response.output_text.delta":
                            # event.delta é um pedaço de texto
                            yield event.delta

                        # Evento final: captura o ID da resposta
                        elif event.type == "response.completed":
                            self.last_response_id = event.response.id

                    # Aguarda qualquer limpeza interna/pós-processo
                    await stream.until_done()

                logger.info("Stream concluído com sucesso.")

            except Exception as exception:
                logger.exception(
                    "Exceção ao obter resposta em stream da API da OpenAI."
                )
                raise
