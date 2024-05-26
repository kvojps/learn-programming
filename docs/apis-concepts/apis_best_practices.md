# Melhores práticas no design de APIs Rest

## URI 
- **Substantivos:** Use substantivos nas URIs para identificar claramente os recursos. Evite verbos, pois as URIs devem representar recursos e não ações. Por exemplo, em vez de **/getUser** use **/users**.
- **Plural:** Utilize o plural para nomear os recursos nas URIs, mesmo que o recurso possa ser único em determinadas operações. Isso torna a nomenclatura consistente e intuitiva. Por exemplo, **/users** em vez de **/user.**
- **Nest resources:** Utilize a aninhamento de recursos (nested resources) para representar a hierarquia e a relação entre recursos. Isso ajuda a organizar e a clarificar a estrutura da API. Por exemplo, para acessar os pedidos de um usuário específico, utilize **/users/{userId}/orders** em vez de algo como **/orders?userId={userId}**;
- **Consistência:** Mantenha consistência na estrutura e no estilo das URIs em toda a API. Isso inclui o uso consistente de maiúsculas/minúsculas, hifens, barras e pluralidade. Isso melhora a previsibilidade e a compreensão da API. Por exemplo, se você começar com **/users**, continue usando essa estrutura para outros recursos, como **/products** e **/categories**;
- **Versioning:** Inclua a versão da API na URI para permitir atualizações e mudanças sem quebrar a compatibilidade com versões anteriores. Isso pode ser feito utilizando um prefixo como /v1, /v2, etc. Por exemplo, /v1/users permite identificar claramente que está utilizando a versão 1 da API.

## Métodos HTTP
- **GET:**
  - **Conjunto de recursos:** Ao obter uma coleção de recursos, você pode aplicar paginação, filtragem e ordenação para controlar o volume e a organização dos dados retornados.
  - **Único recurso:** Solicita um único recurso específico por ID ou identificador único.
  - **Request:**
    - **Headers:** Pode incluir cabeçalhos para controle de cache, como `If-None-Match` ou `If-Modified-Since`.
    - **Body:** Não possui corpo na solicitação GET.

  - **Response:**
    - **Headers:** Pode incluir cabeçalhos para controle de cache, como `ETag` ou `Last-Modified`.
    - **Status code:** 
      - `200 OK`: Quando a solicitação é bem-sucedida e os dados são retornados.
      - `304 Not Modified`: Quando o recurso não foi modificado desde a última solicitação, com base nos cabeçalhos de cache.

- **POST:** Utilizado para criar um novo recurso em uma coleção. A URI alvo geralmente representa a coleção, e o novo recurso é adicionado a esta coleção. Pode ser usado para iniciar uma ação ou processamento específico em um recurso existente.
  - **Request:**
    - **Headers:** Pode incluir cabeçalhos como `Content-Type` para indicar o formato dos dados enviados.
    - **Body:** Inclui o corpo da solicitação com os dados do novo recurso a ser criado ou os parâmetros necessários para a ação a ser iniciada.

  - **Response:**
    - **Headers:** Pode incluir o cabeçalho `Location` indicando a URI do novo recurso criado.
    - **Status code:** 
      - `201 Created`: Quando um novo recurso é criado com sucesso.
      - `202 Accepted`: Quando a solicitação foi aceita para processamento, mas o processamento não foi concluído. Isso é útil para operações assíncronas, onde o cliente não precisa esperar a conclusão do processamento.

- **PUT:** O método PUT é utilizado para criar ou atualizar um recurso específico.
  - **Request:**
    - **Headers:** Pode incluir cabeçalhos como `If-Match` para controle de versões do recurso.
    - **Body:** Deve incluir o recurso completo a ser criado ou atualizado.
  - **Response:**
    - **Headers:** Pode incluir o cabeçalho `Location` indicando a URI do recurso criado ou atualizado.
    - **Status code:**
      - `201 Created`: Quando um novo recurso é criado com sucesso.
      - `200 OK`: Quando um recurso existente é atualizado com sucesso.
      - `204 No Content`: Quando um recurso existente é atualizado com sucesso e não há conteúdo adicional para retornar.
      - `404 Not Found`: Quando o recurso a ser atualizado não é encontrado.
      - `412 Precondition Failed`: Quando a condição especificada nos cabeçalhos, como `If-Match`, falha.

- **DELETE:**
  - **Request:**
    - **Headers:** Pode incluir cabeçalhos como `If-Match` para controle de versões do recurso.
    - **Body:** Não possui corpo na solicitação DELETE.

  - **Response:**
    - **Headers:** Nenhum cabeçalho específico necessário.
    - **Status code:**
      - `204 No Content`: Quando o recurso é removido com sucesso.
      - `412 Precondition Failed`: Quando a condição especificada nos cabeçalhos, como `If-Match`, falha.

## Idempontência
Idempontência refere-se a uma propriedade dos métodos HTTP que garante que realizar a mesma operação múltiplas vezes tenha o mesmo efeito que realizá-la apenas uma vez. Isso é importante para garantir a consistência e previsibilidade das operações na API.

- **GET:** Idempotente. Repetir a solicitação não altera o estado do recurso.
- **PUT:** Idempotente. Repetir a solicitação com os mesmos dados resulta no mesmo estado do recurso.
- **DELETE:** Idempotente. Repetir a solicitação para um recurso já deletado não altera o estado (continua deletado).
- **POST:** Não idempotente. Repetir a solicitação pode resultar na criação de novos recursos duplicados.

## Gerenciamento de Erros
- **4xx: Erros do Cliente** - Ocorrências que indicam que o cliente fez uma solicitação inválida ou incorreta.
- **5xx: Erros do Servidor** - Problemas que surgem devido a falhas no servidor ao processar uma solicitação válida.

## Saiba mais
O conteúdo desta seção foi baseado neste [vídeo.](https://youtu.be/A8t5LSxVJFM?si=3oOuNukYGu-mvg7b)