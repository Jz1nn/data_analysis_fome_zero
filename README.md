# 1. Problema de Negócio

A Fome Zero é uma marketplace de restaurantes que facilita a conexão e negociação entre clientes e restaurantes. O CEO recém-contratado, precisa entender melhor o negócio para tomar decisões estratégicas. Ele contratou você como Cientista de Dados para realizar uma análise detalhada dos dados da empresa e criar dashboards que respondam às perguntas chave sobre o negócio.

# 2. Desafio

O CEO precisa de respostas para as seguintes perguntas para entender melhor a Fome Zero:

## Geral:
1. Quantos restaurantes únicos estão registrados.
2. Quantos países únicos estão registrados.
3. Quantas cidades únicas estão registradas.
4. Qual o total de avaliações feitas.
5. Qual o total de tipos de culinária registrados.

## País:
1. Qual o país com mais cidades registradas.
2. Qual o país com mais restaurantes registrados.
3. Qual o país com mais restaurantes de nível de preço 4.
4. Qual o país com a maior quantidade de tipos de culinária distintos.
5. Qual o país com a maior quantidade de avaliações feitas.
6. Qual o país com a maior quantidade de restaurantes que fazem entrega.
7. Qual o país com a maior quantidade de restaurantes que aceitam reservas.
8. Qual o país com a maior média de avaliações registradas.
9. Qual o país com a maior média de nota registrada.
10. Qual o país com a menor média de nota registrada.
11. Qual a média de preço de um prato para dois por país.

## Cidade:
1. Qual a cidade com mais restaurantes registrados.
2. Qual a cidade com mais restaurantes com nota média acima de 4.
3. Qual a cidade com mais restaurantes com nota média abaixo de 2.5.
4. Qual a cidade com o maior valor médio de um prato para dois.
5. Qual a cidade com a maior quantidade de tipos de culinária distintas.
6. Qual a cidade com a maior quantidade de restaurantes que fazem reservas.
7. Qual a cidade com a maior quantidade de restaurantes que fazem entregas.
8. Qual a cidade com a maior quantidade de restaurantes que aceitam pedidos online.

## Restaurantes:
1. Qual o restaurante com a maior quantidade de avaliações.
2. Qual o restaurante com a maior nota média.
3. Qual o restaurante com o maior valor de um prato para duas pessoas.
4. Qual o restaurante de culinária brasileira com a menor média de avaliação.
5. Qual o restaurante de culinária brasileira no Brasil com a maior média de avaliação.
6. Restaurantes que aceitam pedidos online têm mais avaliações.
7. Restaurantes que fazem reservas têm o maior valor médio de um prato para duas pessoas.
8. Restaurantes de culinária japonesa nos EUA têm um valor médio maior que churrascarias americanas.

## Tipos de Culinária:
1. Restaurante de culinária italiana com a maior média de avaliação.
2. Restaurante de culinária italiana com a menor média de avaliação.
3. Restaurante de culinária americana com a maior média de avaliação.
4. Restaurante de culinária americana com a menor média de avaliação.
5. Restaurante de culinária árabe com a maior média de avaliação.
6. Restaurante de culinária árabe com a menor média de avaliação.
7. Restaurante de culinária japonesa com a maior média de avaliação.
8. Restaurante de culinária japonesa com a menor média de avaliação.
9. Restaurante de culinária caseira com a maior média de avaliação.
10. Restaurante de culinária caseira com a menor média de avaliação.
11. Tipo de culinária com o maior valor médio de um prato para duas pessoas.
12. Tipo de culinária com a maior nota média.
13. Tipo de culinária com mais restaurantes que aceitam pedidos online e fazem entregas.

# 3. Premissas assumidas para a análise

1. Os dados foram coletados da plataforma Kaggle.
2. Os 3 principais visões do negócio foram: Visão por País, visão por cidade e visão por cozinhas.
3. Marketplace foi o modelo de negócio assumido.

# 4. Estratégia da Solução

Para resolver o desafio, será seguido o seguinte roteiro:
1. **Coleta de Dados:** Utilizar o dataset disponível no Kaggle.
2. **Entendimento dos Dados:** Analisar as colunas e remover dados irrelevantes.
3. **Limpeza dos Dados:** Remover duplicatas, verificar e tratar dados faltantes.
4. **Exploração e Análise dos Dados:** Responder às perguntas com base nos dados analisados.
5. **Criação do Dashboard:** Utilizar Streamlit para apresentar os insights de forma visual e acessível.

# 5. Ferramentas Utilizadas

- **Python:** Para análise e manipulação dos dados.
- **Jupyter Lab:** Para prototipar e desenvolver as soluções.
- **Streamlit:** Para criar e hospedar o dashboard interativo.

# 6. Conclusão

- Dashboards interativos que permitam ao CEO visualizar as principais métricas e insights sobre os restaurantes cadastrados na plataforma Fome Zero.
- Respostas detalhadas para todas as perguntas formuladas pelo CEO, baseadas em dados concretos e visualizações claras.

# 7. Próximos Passos

1. Refinar e reduzir o número de métricas apresentadas.
2. Adicionar novos filtros e funcionalidades ao dashboard.
3. Incorporar novas visões de negócio conforme necessário.

# 8. Link do Dashboard

O dashboard pode ser acessado através deste link: [Dashboard Fome Zero](https://johnwln-fome-zero.streamlit.app/)
