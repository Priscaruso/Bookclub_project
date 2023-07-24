# Book Club Project 📚 

🇧🇷

A Book Club é uma startup fictícia de troca de livros, cujo modelo de negócio funciona com base na troca de livros pelos usuários. Cada livro cadastrado pelo 
usuário dá direito à uma troca, mas o usuário também pode comprar o livro, caso ele não queira oferecer outro livro em troca. 

Uma das ferramentas mais importantes para que esse modelo de negócio rentabilize, é a recomendação. Uma excelente recomendação aumenta o volume de 
trocas e vendas no site. No entanto, a empresa não coleta e nem armazena os livros enviados pelos usuários em um banco de dados. Os livros são apenas enviados pelos usuários através de um botão "Fazer Upload", ficando visíveis na plataforma, junto com suas estrelas, que representam o quanto os usuários gostaram do livro.

## Tópicos do projeto

:small_blue_diamond: [Objetivo](#objetivo)

:small_blue_diamond: [Arquitetura dos dados](#arquitetura-dos-dados)

:small_blue_diamond: [Pré-requisitos](#pré-requisitos)

:small_blue_diamond: [Fases do Projeto](#fases-do-projeto)

:small_blue_diamond: [Próximos passos](#próximos-passos)


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
* Criação do banco de dados

  Construção de uma instância RDS PostgreSQL na nuvem AWS para armazenar os dados operacionais da plataforma, conforme mostra a figura abaixo: 
  
  ![Banco de dados RDS](https://github.com/Priscaruso/Bookclub_project/assets/83982164/3212367c-f903-4a63-bef8-c0bcbb9338b7)

   A região selecionada foi a de Oregon nos EUA (us-west-2) e a máquina foi a db.t3.micro por questões de custo e para atender ao volume de dados necessário para esse projeto.
 
* Modelagem dos dados

  Criação do script python [data_model.py] que cria as seguintes funções:
  * Função _check_if_valid_data_ que verifica se os dados coletados apresentam dados ausentes ou não
  * Função _connect_db_ que cria uma conexão com o banco bookclub no RDS usando a url do host, o nome do banco, o usuário padrão do banco, a senha de acesso criada e a porta de conexão. Tanto o usuário como a senha de acesso são armazenados em um arquivo .env no ambiente virtual criado para o projeto, por meio da biblioteca python dotenv, a fim de garantir a segurança dos dados.
  * Função _create_table_ que gera a tabela desejada a partir da execução de uma query, sendo esta tabela armazenada dentro do banco bookclub no RDS. O schema da tabela é apresentado a seguir:
    
    | Column | Data Type |
    | :---: | :---: |
    | id | int autoincremental sequence, PRIMARY KEY |
    | name | varchar(250) |
    | category | varchar(20) |
    | stars | varchar(5) |
    | price | float |
    | availability | varchar(10) |
    
  
 
* Inserção dos dados no banco

  Dentro do script python [data_model.py]() são criadas as seguintes funções:
    * Função _insert_data_ para inserir os dados no banco a partir de uma query e dos valores das variáveis armazenados por meio de uma tupla
    * Função _consulta_db_ que permite realizar consulta dos dados no banco por meio de uma query e retorna os dados na forma de lista

Após a criação das funções, é configurado os parâmetros de navegação para a biblioteca selenium, é criado o objeto de navegação, é chamada a função _get_book_links_ e _get_book_data_ para coletar os dados da plataforma. Os dados são transformados em dataframe, é chamada a função _create_table_ para criar a tabela books dentro do RDS, são realizadas as transformações necessárias nos dados (remoção de apóstrofes e sinais de % em strings) e feita a inserção desses dados na tabela books dentro do banco bookclub no RDS.


### 3ª fase - Construção do Datalake
Nesta fase é criado o Datalake usando o Amazon S3, que é um repositório de objetos. 
São criadas três camadas para armazenar os dados:
  * raw-bookclub - é a camada raw, também conhecida como bronze, onde ficam os dados brutos coletados no seu formato original (geralmente CSV)
  
     ![bucket raw](https://github.com/Priscaruso/Bookclub_project/assets/83982164/e9f615da-84ab-4862-8009-c3b3974541a9)

  
  * processed-bookclub  - é a camada processed, também conhecida como silver, onde ficam os dados que foram transformados para o formato delta, mais otimizado para serem usados na nuvem pelos cientistas e analistas de dados
  
    ![bucket processed](https://github.com/Priscaruso/Bookclub_project/assets/83982164/80bec75d-8486-4ae6-9f6a-9de3302586b8)

  * curated-bookclub - é a camada curated, também conhecida como gold, onde ficam armazenadas as tabelas analíticas, também em formato delta, já transformadas conforme os requisitos da área de negócio, para serem usadas pelos analistas de negócios
  
    ![bucket curated](https://github.com/Priscaruso/Bookclub_project/assets/83982164/8c53685d-6385-4d03-b157-7a1c0f0c62f4)


### 4ª fase - Migração dos dados
Para que as transformações e análises dos dados possam ser realizadas, os dados necessitam estar armazenados em um local apropriado
para isso e que tenha condições de receber constantemente novos dados, ou seja, seja escalável. Assim, o DataLake é o local ideal
para realizar o armazenamento desses dados. Para que isso seja possível, é preciso realizar a migração dos dados brutos contidos no RDS para a camada raw do DataLake (bucket raw-bookclub). Nesse projeto é usado o Database Migration Service da AWS, que apesar de ter um custo mais elevado quando se tem um grande volume de dados, é fácil de usar e realiza a migração de forma mais rápida. A migração é feita de acordo com os seguintes passos:
  * Criar uma instância de replicação no DMS (dms-instance-01)

    A instância é criada na mesma região dos demais serviços, Oregon (us-west) e usando uma máquina dms.t3.micro.
    ![instância de replicação DMS](https://github.com/Priscaruso/Bookclub_project/assets/83982164/bf598a55-b25e-4fc4-a981-487922842d28)

  
  * Criar os endpoints de origem (rds-source-postgresql), que conecta o DMS com o RDS, e de destino (s3-target-datalake), que conecta o DMS com o Datalake S3
  
    ![endpoints](https://github.com/Priscaruso/Bookclub_project/assets/83982164/aa964165-ecc1-4d90-bdf7-94e1937d49b3)

  
  * Testar os endspoints para verificar se a conexão entre o RDS, o DMS e o S3 está funcionando corretamente
    
  
  * Criar uma tarefa de migração (task-01) usando a instância de replicação e os endpoints gerados
  
    ![tarefa de migração parte 2](https://github.com/Priscaruso/Bookclub_project/assets/83982164/5ba7ca5c-df11-4a1d-b0dc-bbce689581b1)


### 5ª fase - Processamento dos dados
Nesta etapa é utilizado o EMR (Elastic Map Reduce) da AWS para realizar o processamento dos dados, usando uma aplicação Spark, que possibilita o processamento de grande volume de dados de forma mais eficiente. A opção por usar o EMR, é que ele é um cluster (uma máquina EC2), que vem com as bibliotecas necessárias já instaladas o que facilita e economiza tempo, além de só cobrar pelo tempo de uso da máquina, podendo processar a quantidade de dados que desejar nesse período, sem ter aumento de custo por conta disso. 
O processamento dos dados consiste nos seguintes passos:
  * Criar um cluster EMR contendo somente a aplicação Spark versão 3.3.0
  
    ![cluster EMR - versão editada](https://github.com/Priscaruso/Bookclub_project/assets/83982164/89a21f7b-3fcf-4ef6-99a4-f2888e5f1515)

  * Criar um job spark por meio de uma aplicação pyspark
  
    O job spark é uma tarefa que será executada pelo cluster EMR, no caso, a aplicação pyspark criada. A aplicação é responsável por fazer as transformações desejadas nos dados e inserí-los na camada processed (bucket processed-bookclub). Ela também gera as tabelas analíticas conforme os requisitos solicitados pela área de negócios e carrega-as tanto na camada curated (bucket curated-bookclub) do datalake como no Data Warehouse, que é o Amazon Redshift. Essa aplicação pyspark de nome [job_spark_app_emr_redshift.py](https://github.com/Priscaruso/Bookclub_project/blob/main/processing/job_spark_app_emr_redshift.py) pode ser encontrada dentro da pasta processing deste repositório.
   


### 6ª fase - Construção do Data Warehouse 

### 7ª fase - Consulta dos dados 

### 8ª fase - Visualização dos dados


## Próximos passos
Com o desejo de evoluir o projeto e torná-lo ainda mais completo, quero incluir nos próximos meses as seguintes funcionalidades:
  * Orquestrar o pipeline usando o Airflow
  * Criar toda infraestrutura como código (IaC) usando o Terraform

------------------------------------------------------------------------------------------------------



