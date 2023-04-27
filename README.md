# Book Club Project 📚 

🇧🇷

A Book Club é uma startup fictícia de troca de livros, cujo modelo de negócio funciona com base na troca de livros pelos usuários. Cada livro cadastrado pelo 
usuário dá direito à uma troca, mas o usuário também pode comprar o livro, caso ele não queira oferecer outro livro em troca. 

Uma das ferramentas mais importantes para que esse modelo de negócio rentabilize, é a recomendação. Uma excelente recomendação aumenta o volume de 
trocas e vendas no site. No entanto, a empresa não coleta e nem armazena os livros enviados pelos usuários em um banco de dados. Os livros são apenas enviados pelos usuários atráves de um botão "Fazer Upload", ficando visíveis na plataforma, junto com suas estrelas, que representam o quanto os usuários gostaram do livro.

_Objetivo_: Criar uma solução para coletar, armazenar e analisar os dados da plataforma web fictícia de troca de livros usando os serviços da nuvem AWS.

Dados desejados:

* Nome do livro
* Categoria do livro
* Número de estrelas
* Preço
* Disponibilidade do livro: em estoque ou não

Link da plataforma: http://books.toscrape.com

## Arquitetura dos dados

## Pré-requisitos
Para executar esse projeto é necessário criar um ambiente virtual, instalar os pacotes Python contidos no arquivo [requirements.txt](https://github.com/Priscaruso/Bookclub_project/blob/main/requirements.txt) e ter uma conta na [AWS](https://aws.amazon.com/pt/console/).

Esse projeto está dividido em fases de construção.

## Fases do Projeto

1ª fase - Criação de um script python utilizando a biblioteca BeautifulSoup para a coleta dos dados e a biblioteca Selenium para a navegação entre as páginas 

O funcionamento do script acontece da seguinte forma:
* Navegação para a página principal da plataforma e print da página utilizando a biblioteca Selenium
* Download da estrutura da página html utilizando a biblioteca BeautifulSoup 
* Navegação por todas as páginas da plataforma, coletando e armazenando os links da página de cada livro encontrado dentro de uma lista
* Navegação por cada página do livro para coletar os dados desejados e armazená-los dentro de um arquivo no formato csv

2ª fase - Modelagem dos dados



### Repositório do Projeto

Nesse repositório encontram-se os seguintes arquivos:
* Script python: bookclub_webscraper.py 
* Arquivo dos dados coletados: data_bookclub.csv


------------------------------------------------------------------------------------------------------



