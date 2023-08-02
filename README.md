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

:small_blue_diamond: [Dificuldades encontradas durante o projeto](#dificuldades-encontradas-durante-o-projeto)

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

 * Criar as databases no Glue Data Catalog
    A database é como se fosse um banco de dados, mas funciona de forma diferente, e é onde são catalogadas as tabelas (metadados), cujos schemas foram inferidos pelo crawler.
   Para criá-la acessa a opção _Databases_ e, em seguida, _adicionar nova database_. Na configuração, define um nome para a database e seleciona o botão _criar database_. Foram criadas duas databases nesse projeto, a  _books-processed_ e a _books-curated_, conforme mostra a figura abaixo:

    ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/1a5e21ae-b771-4eff-bd06-fa0515a66862)
   
    ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/69206d44-f4fc-4997-9ba8-cc62dc4cb1cc)

  * Criar os crawlers no Glue
    
    O Glue é um serviço onde pode-se realizar integrações de dados, ou seja, transportar os dados de um lugar para o outro, realizar transformações nos dados e catalogá-los. Para que os dados do S3 possam ser acessados através do Amazon Athena, é necessário usar o Glue para fazer a integração entre esses dois serviços. O primeiro passo para isso é através do Glue crawler. O crawler vai escanear e inferir automaticamente o schema dos dados transformados armazenados no bucket processed-bookclub e curated-bookclub do S3. Ao criar o crawler, configura-se a fonte dos dados, Delta Lake no caso; o caminho onde está as tabelas do bucket processed-bookclub e do curated-bookclub do S3; habilita a opção criar tabelas nativas para permitir a leitura do formato Delta direto no Athena; um classificador personalizado (algoritmo), que detecta o formato dos dados desejados que será populado no Glue Data Catalog; cria-se um IAM role para o Glue crawler acessar os dados no S3; seleciona a database que vai receber os dados; define que o Glue vai atualizar a definição das tabelas no Data Catalog caso haja alguma alteração no schema dos dados no S3; define uma tabela como depreciada no Data Catalog, caso algum objeto seja deletado na fonte S3; especifica a frequência que o crawler vai ser executado, que no caso é on-demand, sendo executado só quando for desejado. Após o término da sua criação, o crawler é executado clicando no botão _run crawler_. São criados dois crawler nesse projeto, o _crawler-processed-bookclub_ e o _crawler-curated-bookclub_, conforme mostra a figura:
    
     ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/b28ffe8a-7765-4064-bf35-8291aa1e0428)

    Após o término da execução do _crawler-processed-bookclub é gerada a tabela _books_ na database _books-processed_ e o _crawler-curated-bookclub_ gera as tabelas _top10_liked_books_ e _top10_prices_ na database _books-processed_.

    ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/09791d10-2f5a-4dda-96f9-976950cb3751)

  Para acessar os dados no Athena, basta ir na opção _query editor_, selecionar o data source(fonte dos dados) como AWSDataCatalog e a Database desejada, _books-processed_ ou _books-processed_. No menu tables, é possível visualizar as tabelas de cada database. Assim, já consegue-se consultar os dados de cada tabela usando SQL. 
  A figura abaixo mostra o resultado da consulta quando se seleciona todas as colunas da tabela _books_:
  
  ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/fee36a24-fcc0-4589-b22c-5e131740935f)
  ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/4f4b08b7-8ead-47ce-9f74-0bf1291a6bdc)

  Os resultados das consultas ao selecionar todas as colunas das tabelas _top10_liked_books_ e _top10_prices_, respectivamente, também podem ser visualizados a seguir:

  ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/5a6ad7bf-b613-4161-9664-4f6ed7761ec0)
  ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/41d6ada8-d8a6-407c-af7d-3f7bb3f677e0)
  
  ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/f60b5d33-95e0-4f1b-86f2-c4337a76730b)
  ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/30cc304f-5c98-4262-9376-9833299f6fcd)


### 8ª fase - Visualização dos dados
A última etapa do projeto consiste em consumir os dados armazenados no Data Warehouse, o Redshift, por meio de ferramentas de BI para que os analistas de negócios possam tomar melhores decisões por meio da visualização dos dados. Foram usadas duas ferramentas diferentes, o Power BI e o Amazon Quicksight. A escolha por usar essas duas ferramentas é porque o Power BI é a ferramenta de BI mais utilizada no mercado e o Quicksight é fácil de usar, tem um custo mais baixo do que as ferramentas tradicionais como Power BI, além de ser própria da AWS, que foi a nuvem usada durante todo o projeto. 
Para acessar os dados do Redshift por meio do Power BI, é preciso configurar as regras de entrada da VPC onde está o Redshift no console da AWS, para permitir que a conexão do Quicksight chegue até o Redshift. Depois deve-se selecionar a opção "Obter dados" e procurar por "Amazon Redshift". Na tela que se abre, configurar a fonte dos dados colocando o link do endpoint do Redshift e o nome do banco de dados onde as tabelas desejadas se encontram, que é o "dev". Após o estabelecimento da conexão, basta selecionar as tabelas _top10_liked_books_ e _top10_prices_ na nova tela conforme mostrado abaixo:

  ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/a3f9daf5-f8dd-4ae5-acfe-29b8eabdc7ae)

  Com isso, os analistas de negócios já conseguem criar os dashboards e as visualizações de dados desejadas.

  Para acessar os dados a partir do Amazon Quicksight, deve-se criar uma conta nesse serviço usando o usuário da AWS. Esse serviço é pago, mas pode testá-lo gratuitamente por 30 dias. Após a criação da conta, assim como foi feito com o Power BI, deve-se configurar a conexão para acesso do Quicksight ao Redshift. Essa configuração é feita através do Amazon VPC Management Console, por meio do Security Groups (Grupo de Segurança) no painel de navegação conforme os passos abaixo:
  * Um novo Security Group deve ser criado, e nos campos _Tag de Nome_, _Grupo de Nome_ e _Descrição_, inserido o nome _Amazon-QuickSight-access_
  * No campo VPC, colocar o ID da VPC do cluster Redshift que será acessado pelo Quicksight e finalizar a criação do Security Group
  * Em regras de entradas do grupo de segurança, criar uma nova para o Redshift usando a porta TCP do tipo TCP personalizada e número de porta igual ao usado para a porta do banco do cluster Redshift
  *  No campo fonte (source), inserir o bloco de endereço CIDR para Região da AWS onde foi criado a conta do AmazonQuickSight, que nesse caso foi São Paulo, porque essa era a única região no momento que tava disponível para testar grauitamente a ferramenta
  *  Salvar a regra de entrada e navegar até o menu dos clusters do Amazon Redshift Management Console
  *  Exibir as informações do cluster redshift-cluster-1, ir até as configurações de _Rede e de Segurança_, clicar em editar e na opção VPC Security Group, escolher o _Amazon-QuickSight-access_ e salvar as modificações
  *  Ainda no Amazon Redshift Management Console, ir até as configurações de _Rede e de Segurança_ e habilitar o acesso público do cluster
    
 Terminadas as configurações, o próximo passo é acessar o Quicksight através do console da AWS usando a conta criada. Se o Amazon Redshift não estiver configurado como um serviço que o Quicksight pode acessar, ir no menu Segurança e Permissões, e adicioná-lo. Em seguida, ir no menu Dataset e selecionar o Redshift como fonte dos dados. Configurar a nova fonte definindo um nome para ela (_top10_liked_books_ e depois _top10_prices_), uma instância de ID (redshift-cluster-1), o tipo de conexão (Rede pública), o nome do banco de dados (dev), nome de usuário e senha do banco. Após configurar tudo, selecionar conectar para estabelecer a conexão. Em seguida, selecionar o schema e as tabelas desejadas, e o modo de consulta como SPICE, no qual os dados serão armazenados dentro do Quicksight, podendo ser consultados a qualquer momento. Foram criados dois datasets para esse projeto, o _top10_liked_books_ e o _top10_prices_ referentes às tabelas de mesmo nome. As visualizações geradas a partir desses datasets encontram-se a seguir:

  ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/04decfd2-d41c-4958-92c2-745362a39e3c)
  
  ![image](https://github.com/Priscaruso/Bookclub_project/assets/83982164/5df45f7b-3f9c-4205-95e9-ecf7df74c7a3)


A primeira visualização consiste em uma tabela contendo os 10 livros mais curtidos na plataforma pelos usuários e suas respectivas categorias, ou seja, são os livros que tem o maior número de estrelas de acordo com a ordem alfabética. Assim, o fato do livro _#HigherSele: Wake Up Your Life. Free Your Soul. Find Your Tribe._ estar na primeira classificação, não significa que ele tem o maior número de estrelas entre os 10, pois todos esses livros tem 5 estrelas, e sim que é o mais curtido segundo a ordem alfabética.

A segunda visualização mostra os 10 livros mais baratos. O livro _An Abundance of Katherines_ é o que tem o menor preço entre os 1000 livros presentes na plataforma.

Essas são apenas algumas das análises possíveis de serem construídas com as ferramentas de BI. A partir delas, os analistas de negócios já conseguem criar dashboards e diversas outras visualizações de dados, conforme desejado.


## Dificuldades encontradas durante o projeto
Durante o desenvolvimento do projeto, foram encontrados alguns problemas e dificuldades que precisaram ser resolvidos para que cada etapa fosse concluída e assim, atingir o objetivo final do projeto. 
Os problemas foram:
* Erro de conexão do webdriver do navegador firefox com o servidor da página web
* A conexão com a página url da plataforma bookclub não fechava após navegar para a página do último livro desejado
* Erro ao executar a modelagem dos dados, pois o tamanho dos caracteres do campo 'name' da tabela books estava pequeno demais e o campo 'id' da tabela books estava dando como duplicado
* Erro de sintaxe ao tentar inserir strings contendo apóstrofes no banco RDS
* Erro de formato não suportado nas strings ao tentar inserir os dados no banco RDS, pois algumas continham % e o python não reconhece isso
* Falha na conexão com o banco de dados RDS, pois inicialmente a regra de entrada para acesso público ao banco não estava configurada
* Falha no teste de conexão do endpoint do DMS com o RDS por o DMS não suportar a versão do postgres usada no RDS (versão 14.6)
* Erro de módulo não encontrado com o pacote dotenv dentro do cluster EMR ao usar o módulo na aplicação pyspark para salvar as credenciais de acesso, pois o cluster EMR não tinha o dotenv já instalado
* Problema de NoneType na execução da aplicação Pyspark, pois o dataframe não estava sendo atribuído a nenhuma variável dentro da função analytics_table
* Erro ao executar a aplicação Pyspark dentro do cluster EMR pois não estava conseguindo inserir os dados no Redshift devido não ter uma regra de entrada configurada para o acesso público ao Redshift
* Como conectar o Redshift com o Power BI e com o Amazon Quicksight

Para resolver cada uma delas, foi exigido bastante pesquisa e resiliência, algo que faz parte da rotina de quem trabalha com programação e tecnologia. As dificuldades encontradas foram importantes, pois permitaram a evolução do projeto e o meu desenvolvimento profissional, pois só com as dificuldades e os erros que podemos aprender e melhorar cada vez mais.


## Próximos passos
Com o desejo de evoluir o projeto e torná-lo ainda mais completo, quero incluir nos próximos meses as seguintes funcionalidades:
  * Orquestrar o pipeline usando o Airflow
  * Criar toda infraestrutura como código (IaC) usando o Terraform

------------------------------------------------------------------------------------------------------



