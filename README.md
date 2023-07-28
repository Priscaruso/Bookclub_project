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
para realizar o armazenamento desses dados. Para que isso seja possível, é preciso realizar a migração dos dados brutos contidos no RDS para a camada raw do DataLake (bucket raw-bookclub). Nesse projeto é usado o Database Migration Service (DMS) da AWS, que pode realizar a migração de banco de dados do ambiente on-premise para a nuvem ou da própria nuvem para outro local na nuvem, gerenciar a migração tanto de dados full como de dados incrementais por meio do Change Data Capture (CDC). Tem um custo razoável, é fácil de usar e realiza a migração de forma mais rápida. A migração é feita de acordo com os seguintes passos:
  * Criar uma instância de replicação no DMS

    A instância é criada com o nome _dms-instance-01_ na mesma região dos demais serviços, Oregon (us-west-2), com uma engine na versão 3.4.6, uma máquina dms.t3.micro, que tem uma memória menor, e no ambiente de dev/teste. O ideal é selecionar uma mémoria que corresponda, no mínimo, ao tamanho de memória do banco de dados de origem para que não haja problemas de memória. Em relação ao espaço de armazenamento, deve ter no mínimo metade do tamanho do banco de dados de origem. Essa instância é responsável pelo gerenciamento da tarefa de migração.
    
    ![instância de replicação DMS](https://github.com/Priscaruso/Bookclub_project/assets/83982164/bf598a55-b25e-4fc4-a981-487922842d28)

  * Criar os endpoints de origem (rds-source-postgresql), que conecta o DMS com o RDS, e de destino (s3-target-datalake), que conecta o DMS com o Datalake S3
  
    ![endpoints](https://github.com/Priscaruso/Bookclub_project/assets/83982164/aa964165-ecc1-4d90-bdf7-94e1937d49b3)

  
  * Testar os endspoints para verificar se a conexão entre o RDS, o DMS e o S3 está funcionando corretamente
    
  
  * Criar uma tarefa de migração (task-01) usando a instância de replicação e os endpoints gerados
  
    A tarefa é responsável por fazer a conexão entre os endpoints, ou seja, o banco de dados de origem e de destino, e é executada pela instância de replicação.
  
  ![tarefa de migração parte 2](https://github.com/Priscaruso/Bookclub_project/assets/83982164/5ba7ca5c-df11-4a1d-b0dc-bbce689581b1)
    
  Após a conclusão da tarefa de migração, os dados terão sido movidos para o bucket raw-bookclub do Datalake.


  ### 5ª fase - Construção do Data Warehouse 
O Data Warehouse é o armazém de dados analíticos, onde os analistas de negócios conseguem obter insights por meio de consultas SQL e também servir os dados para as ferramentas analíticas de visualização gerarem dashboards, que permitem a eles tomar melhores decisões. O Data Warehouse utilizado nesse projeto é o Amazon Redshift, uma das soluções mais usadas no mercado, que armazena as tabelas analíticas geradas de acordo com as regras de negócios na etapa de processamento dos dados. O Redshift possui um cluster com vários nós (máquinas), o que permite escalar a performance das consultas, além de possuir diversos outros recursos para escabilidade e alta performance.
Para construir o Data Warehouse, precisa-se criar um cluster, conforme os passos abaixo:
  * definir o nome do cluster, no caso redshift-cluster-1
  * selecionar um nó (servidor) do tipo dc2.large (nível gratuito/free-tier)
  * definir um usuário e uma senha para acesso ao banco de dados que será criado dentro do cluster
A figura abaixo mostra o cluster gerado:

  ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/bb0494fb-2889-4dcf-8890-727ee2771694)

O acesso ao Redshift se dá através do editor de consultas v2 (query editor v2) no qual pode-se realizar consultas SQL nas tabelas analíticas geradas através da aplicação pyspark no processamento dos dados.


### 6ª fase - Processamento dos dados
Nesta etapa foi utilizado o EMR (Elastic Map Reduce) da AWS para realizar o processamento dos dados, usando uma aplicação Spark, que possibilita o processamento de grande volume de dados de forma mais eficiente. A opção por usar o EMR, é que ele é um cluster (uma máquina EC2), que pode vir instalado com diversas aplicações open source do ecossistema Hadoop e tem as bibliotecas necessárias (como as para o formato Delta) e os JARS necessários para trabalhar com Redshift já instalados, o que facilita e economiza tempo. Além disso, ele só cobra pelo tempo de uso da máquina, podendo processar a quantidade de dados que desejar nesse período, sem ter aumento de custo por conta disso. 
O processamento dos dados consiste nos seguintes passos:
  * Criar um cluster EMR contendo somente a aplicação Spark versão 3.3.0
    
    Foi usado o EMR versão 6.9.0 que já vem com as bibliotecas Delta e máquinas EC2 do tipo m4.large, que tem menor custo e menor recurso computacional, mas atende ao objetivo do projeto. Durante a criação do cluster, é necessário gerar um par de chaves SSH no formato PEM para acessar as máquinas EC2 do cluster EMR. Além disso, também é necessário criar as roles de acesso a serviços da AWS (EMR_DefaultRole_V2), que permitem o acesso do EMR ao S3 para armazenar os dados processados, e de acesso a instâncias EC2 (EMR_EC2_DefaultRole), para provisionar as máquinas do cluster.
  
    ![cluster EMR - versão editada](https://github.com/Priscaruso/Bookclub_project/assets/83982164/89a21f7b-3fcf-4ef6-99a4-f2888e5f1515)

  * Criar um job spark por meio de uma aplicação pyspark
  
    O job spark é uma tarefa que será executada pelo cluster EMR, no caso, a aplicação pyspark criada. A aplicação é responsável por fazer as transformações desejadas nos dados e inserí-los na camada processed (bucket processed-bookclub). Ela também gera as tabelas analíticas conforme os requisitos solicitados pela área de negócios e carrega-as tanto na camada curated (bucket curated-bookclub) do datalake como no Data Warehouse, que é o Amazon Redshift. Essa aplicação pyspark de nome [job_spark_app_emr_redshift.py](https://github.com/Priscaruso/Bookclub_project/blob/main/processing/job_spark_app_emr_redshift.py) pode ser encontrada dentro da pasta processing deste repositório.
   
Para executar o job spark necessita-se:
  * habilitar a permissão de execução para o proprietário do arquivo do par de chaves SSH: `chmod 400 local_das_chaves`, onde local_das_chaves é a pasta onde o par de chaves SSH foi salvo
  * mover a aplicação criada para dentro do diretório padrão do Hadoop no cluster EMR, conforme o comando `scp -i local_das_chaves job-spark-app-emr-redshift.py hadoop@url_do_servidor:/home/hadoop/`, onde url_do_servidor é o link do DNS público do nó primário (servidor master do EMR) localizado na console da AWS a partir das informações do cluster-bookclub
  * conectar remotamente no servidor master usando ssh: `ssh -i local_das_chaves hadoop@url_do_servidor`
  * executar o comando spark-submit para rodar a aplicação:
    
    `spark-submit --packages io.delta:delta-core_2.12:2.0.0 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog"  --jars /usr/share/aws/redshift/jdbc/RedshiftJDBC.jar,/usr/share/aws/redshift/spark-redshift/lib/spark-redshift.jar,/usr/share/aws/redshift/spark-redshift/lib/spark-avro.jar,/usr/share/aws/redshift/spark-redshift/lib/minimal-json.jar job-spark-app-emr-redshift.py`
    
O comando acima faz a configuração das bibliotecas Delta, para gerar os dados nesse formato, e JARS, para o EMR conseguir trabalhar junto com o Redshift, executando logo em seguida, a aplicação.
Ao concluir a execução da aplicação, os dados transformados em formato delta estarão localizados no bucket processed-bookclub e as tabelas analíticas _top10_liked_books_ e _top10_prices_ geradas a partir deles, no bucket curated-bookclub e no Redshift.


### 7ª fase - Consulta dos dados 
Essa etapa consiste no acesso aos dados analíticos já transformados, de acordo com as regras de negócios definidas, por meio do Amazon Athena. O Athena é um serviço serverless (sem necessidade de provisionar servidor) de consultas ad-hoc simples, onde os analistas de negócios podem rapidamente realizar consultas interativas de forma simples para obter os insights desejados a partir dos dados tratados que estão armazenados no S3, no caso desse projeto são os que se encontram na camada curated do Datalake, o bucket curated-bookclub. O custo dele é por consulta, por quantidade de terabyte escaneado, assim o ideal é tentar definir um limite usando workgroups (grupos de trabalho) para obter os insights desejados utilizando o menor número de consultas possível. Para acessar esses dados no Athena, primeiramente, devem ser realizados os seguintes passos:

  * Criar um crawler no Glue
    O crawler vai escanear e inferir automaticamente o schema dos dados transformados armazenados no bucket curated-bookclub do S3.
    
  * criar uma database no Glue Data Catalog
    A database é como se fosse um banco de dados, mas de fato não é, 

### 8ª fase - Visualização dos dados

## Problemas encontrados

## Próximos passos
Com o desejo de evoluir o projeto e torná-lo ainda mais completo, quero incluir nos próximos meses as seguintes funcionalidades:
  * Orquestrar o pipeline usando o Airflow
  * Criar toda infraestrutura como código (IaC) usando o Terraform

------------------------------------------------------------------------------------------------------



