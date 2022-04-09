# Book Club Project

A Book Club é uma startup fictícia de troca de livros, cujo modelo de negócio funciona com base na troca de livros pelos usuários. Cada livro cadastrado pelo 
usuário dá direito à uma troca, mas o usuário também pode comprar o livro, caso ele não queira oferecer outro livro em troca. 

Uma das ferramentas mais importantes para que esse modelo de negócio rentabilize, é a recomendação. Uma excelente recomendação aumenta o volume de 
trocas e vendas no site. No entanto, a empresa não coleta e nem armazena os livros enviados pelos usuários em um banco de dados. Os livros são apenas enviados pelos usuários atráves de um botão "Fazer Upload", ficando visíveis na plataforma, junto com suas estrelas, que representam o quanto os usuários gostaram do livro.

Objetivo: Criar uma solução para coletar e armazenar os dados da plataforma web fictícia de troca de livros.

Dados desejados:

-Nome do livro
-Categoria 
-Número de estrelas
-Preço
-Disponibilidade do livro: em estoque ou não

Link da plataforma: http://books.toscrape.com

Esse projeto foi dividido em fases de construção.

### Fases do Projeto

1º fase - Criação de um script python utilizando a biblioteca BeautifulSoup para a coleta dos dados e a biblioteca Selenium para a navegação entre as páginas 

O funcionamento do script acontece da seguinte forma:
-Navegação para a página principal da plataforma e print da página utilizando a biblioteca Selenium
-Download da estrutura da página html utilizando a biblioteca BeautifulSoup 
-Navegação por todas as páginas da plataforma, coletando e armazenando os links da página de cada livro encontrado dentro de uma lista
-Navegação por cada página do livro para coletar os dados desejados e armazená-los dentro de um arquivo no formato csv

