from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import dotenv
import os

#  Spark applcation setup
spark = SparkSession \
    .builder \
    .appName("job-1-spark") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# application logging method
spark.sparkContext.setLogLevel("ERROR")

def read_csv(bucket, path):
    """Function that reads csv file from s3 


    :param bucket: str the bucket url which contains the file
    :param path: str the csv file path
    :return: dataframe - pyspark dataframe which the csv file was transformed into

    It reads the csv file using the url location of the bucket and the file path, reading the file header, infering its
    schema and transforming it into a dataframe. The first 5 lines of the dataframe and its schema are printted out, 
    returning the dataframe.
    """

    # reading data from Data Lake
    df = spark.read.format("csv")\
        .option("header", "True")\
        .option("inferSchema", "True")\
        .csv(f"{bucket}/{path}")
    
    # print data from raw bucket
    print ("\nImprime os dados lidos da raw:")
    print(df.show(5))
    # print dataframe schema    
    print("\Imprime o schema do dataframe")
    print(df.printSchema())
    return df

def read_delta(bucket, path):
    """Function that reads delta file from s3 


    :param bucket: str the bucket url which contains the file
    :param path: str the delta file path
    :return: dataframe - pyspark dataframe which the delta file was transformed into

    It reads the delta file using the url location of the bucket and the file path inside the bucket, transforming it
    into a dataframe and returning the dataframe.
    """

    df = spark.read.format("delta")\
        .load(f"{bucket}/{path}")
    return df

def write_processed(bucket, path, dataframe, col_partition, data_format, mode):
    """Function that writes data in the processed zone (bucket)

    :param bucket: str the bucket url where the file will be written
    :param path: str the path where the file will be written
    :param dataframe: dataframe the dataframe that contains the data
    :param col_partition: str the column used to partitionate the data
    :param data_format: str the format which the file will be written in the bucket
    :param mode: str the mode used to write the data
    :return: int - returns 0 if the data is written in the processed zone and 1 if an error is generated

    It writes data in the path inside the processed zone bucket, using the partition, the format and the mode specified. 
    It returns 0 if the data is sucessfully written in the bucket, and 1 if an error occurs.
    """

    print("\nWritting delta data in the processing zone...")
    try:
        dataframe.write.format(data_format)\
            .partitionBy(col_partition)\
            .mode(mode)\
            .save(f"{bucket}/{path}")
        print(f"Data sucessfully written in the processed zone")
        return 0
    except Exception as error:
        print(f"Failed to write data in the processed zone: {error}")
        return 1

def write_curated(bucket, path, dataframe, data_format, mode):
    """Function that writes data in the curated zone (bucket)

    :param bucket: str the bucket url where the file will be written
    :param path: str the path where the file will be written
    :param dataframe: dataframe the dataframe that contains the data
    :param data_format: str the format which the file will be written in the bucket
    :param mode: str the mode used to write the data
    :return: int - returns 0 if the data is written in the curated zone and 1 if an error is generated

    It writes data in the path inside the curated zone bucket, using data from the dataframe, transforming it into 
    the format and using the mode specified. 
    It returns 0 if the data is sucessfully written in the bucket, and 1 if an error occurs.
    """
    # convert processed data to parquet and write it in the curated zone
    print("\nWritting data into the curated zone...")
    try:
        dataframe.write.format(data_format)\
            .mode(mode)\
            .save(f"{bucket}/{path}")
        print("Data was sucessfully written in the curated zone!")
        return 0
    except Exception as error:
        print(f"Failed to write data in the curated zone: {error}")
        return 1

def write_redshift(url_jdbc, user, password, table_name, dataframe):
    """Function that writes data into Redshift

    :param url_jdbc: str the redshift jdbc driver url
    :param user: str the name of the user to access redshift
    :param password: str the password to access redshift
    :param table_name: str the name of the table to be created inside redshift
    :param dataframe: dataframe the pyspark datafram which contains the data
    :return: int - returns 0 if the data is written in redshift and 1 if an error is generated

    It writes data in a table inside redshift using the jdbc driver url, the name of the user and the password of redshift,
    using data from the specified dataframe.
    It returns 0 if the data is sucessfully written in redshift, and 1 if an error occurs.
    """

    try:
        dataframe.write.format("jdbc")\
            .options(url=url_jdbc,
                 driver="com.amazon.redshift.jdbc42.Driver",
                 user=user,
                 password=password,
                 dbtable=table_name)\
            .mode("overwrite")\
            .save()
        print("Data was sucessfully written into Redshift!")
        return 0
    except Exception as error:
        print(f"Failed to write data into Redshift: {error}")
        return 1


def analytics_table(bucket, dataframe, table_name, user, password, flag_write_redshift, url_jdbc):
    """Function that creates analytics tables and writes them in the curated zone, and in Redshift
    
    :param bucket: str the bucket url where the table will be written
    :param dataframe: dataframe the dataframe that contains the data
    :param table_name: str the name of the table that will be generated in the bucket
    :param user: str the user used to access redshift
    :param password: str the password used to access redshift
    :param flag_write_redshift: bool the flag used to verify if shoud write data to redshift or not
    :param url_jdbc: str the redshift jdbc driver url

    It creates analytics tables inside the bucket in the curated zone and in redshift, using data from the specified 
    dataframe, the user name and the password of redshift, the state of the redshift flag, and jdbc driver url.
    """
    # creates a view for the dataframe
    dataframe.createOrReplaceTempView(table_name)

    # creates a new column with stars mapped from strings to integers
    dataframe = dataframe.withColumn("stars_numbers", 
                                    when(col("stars") == "One", 1)
                                    .when(col("stars") == "Two", 2)
                                    .when(col("stars") == "Three", 3)
                                    .when(col("stars") == "Four", 4)
                                    .otherwise(5))

    # processes data according to business rules
    # generates the top 10 most liked books in alphabetical order
    df_1 = dataframe.select(col("name"), col("category"), col("stars_numbers")) \
            .sort(desc("stars_numbers"), asc("name")) \
            .limit(10)
    # generates the top 10 most cheapest books
    df_2 = dataframe.select(col("name"), col("category"), col("price")) \
            .sort(asc("price"))\
            .limit(10)
    
    # print the created dataframe
    print("\n Top 10 most liked books")
    print(df_1.show())
    print("\n Top 10 most cheapest books")
    print(df_2.show())
    write_curated(f"{bucket}", "top10_liked_books", df_1, "delta", "overwrite")
    write_curated(f"{bucket}","top10_prices", df_2, "delta", "overwrite")

    # writes data to redshift when flag_write_redshift is true
    if flag_write_redshift == True:
        write_redshift(url_jdbc, user, password, "top10_liked_books", df_1)
        write_redshift(url_jdbc, user, password, "top10_prices", df_2)

# read csv data from raw zone
df = read_csv("s3a://raw-bookclub","public/books/")

# process and write partitioned delta data by stars in processed zone
write_processed("s3a://processed-bookclub", "books", df, "stars", "delta", "overwrite")

# read delta data from processed zone
df = read_delta("s3a://processed-bookclub", "books/")

# sets the system to use the user, the password and the jdbc url from the .env file
dotenv.load_dotenv(dotenv.find_dotenv())
user = os.getenv("user")
password = os.getenv("password")
url_jdbc = os.getenv("url_jdbc")

# sets the write redshift flag 
flag_write_redshift = True

# creates the analytics tables in the curated zone and in Redshift
analytics_table("s3a://curated-bookclub", df, "books", user, password, flag_write_redshift, url_jdbc)

# stop the application
spark.stop()