<h1><p align="center"><b>AmicusDei – Assistente Teológico Católico (RAG Chatbot)</b></p></h1>

<p align="center">
<a href="https://amicusdei.streamlit.app/"><img src="src/img/amicusdei.svg" alt="capa do AmicusDei"></a>
</p>

> **Status**: *Em desenvolvimento* ⚙️

<h2 align="center"><p><a href="https://amicusdei.streamlit.app/"><u>Clique aqui para usar o AmicusDei!</u></a></p></h2>

<div style="margin: 40px;"></div>

# Objetivos do Projeto

O **AmicusDei** nasceu para mostrar, na prática, como a [**API RAG do Catecismo da Igreja Católica**](https://catholic-catechism-rag-api.aight.com.br/) pode servir de base para aplicações digitais que aproximam as pessoas da fé. Ele oferece um espaço acolhedor para quem está chegando ou retornando à Igreja, com respostas ancoradas no Catecismo da Igreja Católica (CIC) e disponíveis a qualquer hora.

A partir desse propósito, o projeto também virou um laboratório onde aplico LLMs, RAG e boas práticas de arquitetura. O Streamlit funciona como a porta de entrada do chat, a API RAG entrega os parágrafos oficiais do Catecismo, e a OpenAI monta a resposta final em tempo real, garantindo fidelidade doutrinária e acessibilidade para qualquer pessoa.

<div style="margin: 20px;"></div>

# Arquitetura e Fluxo do Assistente

1) **Validação ética do questionamento**  
   - Na primeira interação, a pergunta é enviada à API RAG, que já valida tamanho, clareza e escopo catequético antes de devolver qualquer referência.
   - Nas mensagens seguintes, o QueryValidator local reavalia a adequação do que o usuário envia, bloqueando conteúdos impróprios ou fora de contexto.

2) **RAG com o Catecismo**  
   - As perguntas válidas consultam a [API RAG do Catecismo da Igreja Católica](https://catholic-catechism-rag-api.aight.com.br/) que devolve os 3 parágrafos mais similares, com pontuação de similaridade e localização atual dentro da estrutura do Catecismo.

3) **Geração de respostas streaming**  
   - Quando os parágrafos são úteis, eles alimentam o prompt do modelo `gpt-5-mini`.  
   - O retorno usa streaming para garantir baixa latência e permitir UX fluida no chat.

4) **Orquestração do front-end**  
   - O Streamlit controla estado de conversa (até 3 interações), expõe descrições auxiliares, registra histórico e trata erros de domínio/servidor para manter o usuário informado.

<div style="margin: 20px;"></div>


# Estrutura de Pastas do Projeto

```
catholic-catechism-rag-chatbot/
├── chatbot.py                         # Camada de apresentação (Streamlit)
├── src/
│   ├── config/logger_config.py        # Configuração de logs
│   ├── data/
│   │   ├── chatbot_descriptions/      # Descrições para a UI 
│   │   └── prompt/                    # Instruções do modelo
│   ├── domain/
│   │   ├── services/query_validator.py
│   │   └── use_cases/CatholicCatechismChatBot.py
│   ├── errors/                        # Exceções de domínio/servidor
│   ├── infra/openai_api/              # Abstrações de consumo da OpenAI
│   └── validators/models/             # Modelos Pydantic utilizados
├── src/img/amicusdei_capa.svg         # Arte utilizada no README e na UI
└── LICENSE                            # MIT License
```

<div style="margin: 20px;"></div>


# Referências
CATECISMO DA IGREJA CATÓLICA. Edição típica vaticana. Disponível em: https://www.vatican.va/archive/cathechism_po/index_new/prima-pagina-cic_po.html

OPENAI. Documentation. Disponível em: https://platform.openai.com/docs/. 

STREAMLIT. Documentation. Disponível em: https://docs.streamlit.io/.

<hr></hr> <div style="margin: 20px;"></div> <p align="center">Para acompanhar evoluções do projeto, siga as atualizações neste repositório.</p> <p align="center">Que Deus te abençoe! 🙏</p>