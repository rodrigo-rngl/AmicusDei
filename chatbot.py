
import os
import asyncio
import inspect
import nest_asyncio
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from typing import AsyncGenerator, Literal
from src.errors.types.server_error import ServerError
from src.domain.use_cases.CatholicCatechismChatBot import CatholicCatechismChatBot

nest_asyncio.apply()

load_dotenv()


def start_history_messages() -> None:
    if st.session_state.history_messages:
        for message_dict in st.session_state.history_messages:
            with st.chat_message(message_dict['role']):
                st.markdown(message_dict['content'])


def start_css_styles(height: int = 100) -> None:
    st.markdown(f"""
    <style>
    .center-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: {height}px; 
    }}
    </style>
    """, unsafe_allow_html=True)


def initialize_sessions_states() -> None:
    if "history_messages" not in st.session_state:
        st.session_state.history_messages = []

    if "chatbot_service" not in st.session_state:
        st.session_state.chatbot_service = CatholicCatechismChatBot(
            prompt_id=str(st.secrets["PROMPT_CHATBOT_ID"]))

    if "conversation_chat" not in st.session_state:
        st.session_state.conversation_chat = st.empty()

    if "last_query" not in st.session_state:
        st.session_state.last_query = ""

    if "interactions_counter" not in st.session_state:
        st.session_state.interactions_counter = 0


def write_how_to_work_description() -> None:
    description_path = Path(
        "src/data/chatbot_descriptions/how_to_work.md")
    description = description_path.read_text(encoding="utf-8")

    with st.expander("ℹ️ Como funciona o **AmicusDei**?", expanded=False):
        st.markdown(description, unsafe_allow_html=False)


def write_about_description() -> None:
    description_path = Path(
        "src/data/chatbot_descriptions/about.md")
    description = description_path.read_text(encoding="utf-8")

    st.markdown(description, unsafe_allow_html=False)


def store_history_messages(role: Literal['user', 'assistant'], text) -> None:
    st.session_state.history_messages.append({"role": role, "content": text})


def get_first_user_query() -> None:
    with st.session_state.conversation_chat.container(border=False):
        st.markdown(
            f'<div class="center-container">', unsafe_allow_html=True)

        st.markdown(
            f"<h2 style='text-align: center;'>Qual dúvida posso te esclarecer sobre a doutrina da Igreja Católica?</h2>", unsafe_allow_html=True)

        query = st.chat_input('Pode perguntar...')
        st.markdown('</div>', unsafe_allow_html=True)

    if not query:
        st.stop()

    st.session_state.last_query = query
    st.session_state.conversation_chat.empty()


def get_next_user_query() -> None:
    query = st.chat_input('Mais alguma dúvida?')

    if query:
        st.session_state.last_query = query

        st.session_state.conversation_chat.empty()
        st.rerun()

    st.session_state.last_query = ""
    st.stop()


def post_user_query(user_query: str) -> None:
    with st.chat_message("user"):
        st.markdown(user_query)


async def get_assistant_response(user_query: str) -> AsyncGenerator[str, None] | str:
    response = await st.session_state.chatbot_service.generate_assistant_response(
        user_message=user_query)

    return response


def post_assistant_response(response: AsyncGenerator[str, None] | str):
    with st.chat_message("assistant"):
        # Sucesso
        if inspect.isasyncgen(response):
            with st.spinner("Respondendo...", show_time=True):
                stream_response = st.write_stream(response)

            return stream_response

        # Exceção
        st.markdown(response)
        return response


async def generate_assistant_response(user_query: str):
    try:
        with st.spinner("Gerando resposta...", show_time=True):
            response = await get_assistant_response(user_query)

        complete_response = post_assistant_response(response)

        return complete_response

    except ServerError as error:
        st.warning(error.body['warning_message'])
        st.stop()


async def main() -> None:
    st.set_page_config(
        page_title="AmicusDei – Assistente Teológico Católico",
        initial_sidebar_state="expanded")

    write_how_to_work_description()

    st.sidebar.image('src/img/amicusdei_capa.svg')
    with st.sidebar.expander("💡 **Sobre este projeto!**", expanded=True):
        write_about_description()
    st.sidebar.caption(
        "Feito por [Rodrigo Rangel](www.linkedin.com/in/rodrigo-rngl/). Ofertado a Deus por *São Carlo Acutis* e *Santa Teresinha*!")

    initialize_sessions_states()
    start_css_styles()

    if st.session_state.interactions_counter == 0:
        get_first_user_query()

    with st.session_state.conversation_chat.container(border=True):
        if st.session_state.interactions_counter > 0:
            start_history_messages()

        if st.session_state.last_query:
            query = st.session_state.last_query

            post_user_query(query)
            store_history_messages(role='user', text=query)

            complete_response = await generate_assistant_response(query)
            store_history_messages(
                role='assistant', text=complete_response)

            st.session_state.interactions_counter += 1

        if st.session_state.interactions_counter >= 3:
            st.info(
                "Já não posso receber mais respostas! Obrigado por sua participação!")
            st.stop()

        get_next_user_query()


def run_app() -> None:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(main())


run_app()
