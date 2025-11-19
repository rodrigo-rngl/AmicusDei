import os
from openai import AsyncOpenAI

from src.config.logger_config import setup_logger
logger = setup_logger(name="OpenAIAPIConnectionHandler")


class OpenAIAPIConnectionHandler:
    def __init__(self) -> None:
        self.__api_key = os.getenv("OPENAI_API_KEY")

        self.client = self.__create_api_client()

    def __create_api_client(self) -> AsyncOpenAI:
        try:
            return AsyncOpenAI(
                api_key=self.__api_key
            )
        except Exception as exception:
            logger.error(f'Exceção ao gerar conexão com a API da OpenAI.\n'
                         f'Exception: {exception}')
            raise

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()
