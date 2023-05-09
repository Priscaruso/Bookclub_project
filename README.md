# Book Club Project 📚 

🇧🇷

A Book Club é uma startup fictícia de troca de livros, cujo modelo de negócio funciona com base na troca de livros pelos usuários. Cada livro cadastrado pelo 
usuário dá direito à uma troca, mas o usuário também pode comprar o livro, caso ele não queira oferecer outro livro em troca. 

Uma das ferramentas mais importantes para que esse modelo de negócio rentabilize, é a recomendação. Uma excelente recomendação aumenta o volume de 
trocas e vendas no site. No entanto, a empresa não coleta e nem armazena os livros enviados pelos usuários em um banco de dados. Os livros são apenas enviados pelos usuários através de um botão "Fazer Upload", ficando visíveis na plataforma, junto com suas estrelas, que representam o quanto os usuários gostaram do livro.

## Tópicos do projeto

:small_blue_diamond: [Arquitetura dos dados](#arquitetura-dos-dados)

:small_blue_diamond: [Pré-requisitos](#pré-requisitos)

:small_blue_diamond: [Fases do Projeto](#fases-do-projeto)

:small_blue_diamond: [Execução](#execução-do-projeto)


## Objetivo
Criar uma solução para coletar, armazenar e analisar os dados da plataforma web fictícia de troca de livros usando os serviços da nuvem AWS.

Dados desejados:

* Nome do livro
* Categoria do livro
* Número de estrelas
* Preço
* Disponibilidade do livro: em estoque ou não

Link da plataforma: http://books.toscrape.com


## Arquitetura dos dados
A arquitetura do projeto utiliza os serviços da nuvem AWS aplicados à engenharia de dados, conforme mostra a figura a seguir:

![Arquitetura dos dados](https://user-images.githubusercontent.com/83982164/235518227-0165070a-5b47-459f-b75b-dd99b56203b3.png)



## Pré-requisitos
Para executar esse projeto é necessário criar um ambiente virtual, instalar os pacotes Python contidos no arquivo [requirements.txt](https://github.com/Priscaruso/Bookclub_project/blob/main/requirements.txt) e ter uma conta na [AWS](https://aws.amazon.com/pt/console/).

Esse projeto está dividido em fases de construção.

## Fases do Projeto

### 1ª fase - Coleta dos dados

Criação do script python [bookclub_webscraper.py](https://github.com/Priscaruso/Bookclub_project/blob/main/bookclub_webscraper.py) que define as funções para a coleta dos dados da plataforma.

O funcionamento do script acontece da seguinte forma:
* Função _"get_book_links"_ navega por todas as páginas da plataforma, coletando e armazenando os links da página de cada livro encontrado dentro de uma lista usando as bibliotecas Selenium e BeautifulSoup 
* Função _"get_book_data"_ navega por cada página do livro para coletar os dados desejados e armazená-los dentro de uma lista

### 2ª fase - Armazenamento dos dados

Essa fase é subdividida em 3 passos:
* Modelagem dos dados
  Criação do script python [data_model.py] que cria a tabela book que será armazenado dentro do banco books no RDS.  
  
* Criação do banco de dados
 Construção de um cluster RDS na nuvem AWS para armazenar os dados, conforme mostra a figura abaixo: 

* Inserção dos dados no banco
  Dentro do script python [data_model.py]() é chamada a função _"get_book_data"_ para coletar os dados da plataforma e poder realizar a inserção desses dados na tabela books dentro do banco no RDS.
  
### 3ª fase - Construção do Datalake

### 4ª fase - Migração dos dados

### 5ª fase - Processamento dos dados

### 6ª fase - Construção do Data Warehouse 

### 7ª fase - Consulta dos dados 

### 8ª fase - Visualização dos dados



### Repositório do Projeto

Nesse repositório encontram-se os seguintes arquivos:
* Script python: bookclub_webscraper.py 
* Arquivo dos dados coletados: data_bookclub.csv


------------------------------------------------------------------------------------------------------



