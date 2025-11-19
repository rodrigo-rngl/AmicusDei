### 📖 **Como funciona o Assistente Teológico?**
O Assistente Teológico AmicusDei tem o intuito de esclarecer alguma dúvida pertinente sobre teologia e/ou doutrina católica que possa surgir no seu processo de conversão, sempre utilizando o Catecismo da Igreja Católica como referência. O assistente foi configurado para responder um único questionamento central, e gerar mais 2 respostas para questionamentos que possam surgir em você, derivados da resposta do assistente ao questionamento central.

O fluxo de execução do assistente funciona da seguinte forma:
1. Busca os **parágrafos do Catecismo da Igreja Católica mais similares** (em comparação ao questionamento válido realizado pelo usuário), através da [API RAG do Catecismo da Igreja Católica](https://catholic-catechism-rag-api.aight.com.br/) também desenvolvida por mim;
    - Se o questionamento não for válido, o assitente irá sinalizar ao usuário, ou irá solicitar ao e cliente que aprimore o questionamento anteriormente enviado.
2. Analisa se o conteúdo teológico retornado pela API é útil para responder o questionamento do usuário. 
    - Se o conteúdo for útil, utiliza os parágrafos do CIC para alimentar o contexto de um modelo de linguagem de grande escala para retornar a resposta;
    - Se não for útil, utiliza apenas o modelo de linguagem de grande escala para retornar a resposta, sem alimentação de contexto;
3. Gera resposta com fundamentação oficial e **citação integral** dos parágrafos do CIC utilizados, com tom **catequético, pastoral, fiel, clara e acolhedor**, como faria um **teólogo católico da sua paróquia**.

Para utilizar o Assistente Teológico AmicusDei da melhor forma, apresente todos os detalhes possíveis sobre sua dúvida, pois fazendo assim, haverá mais chances do assistente teológico te ajudar de forma precisa.

Também lembre-se que você só poderá realizar até 3 interações com o assistente. Use-as com sabedoria!