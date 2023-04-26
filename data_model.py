# it imports the libraries
from bookclub_webscraper import get_book_links, get_book_data
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import psycopg2
import dotenv
import os


# checks data quality
def check_if_valid_data(df: pd.DataFrame) -> bool:
    """Functions that checks if data doesn't contain missing values, being considered as valid

    :param df: pd.DataFrame - dataframe used to check the data
    :return: bool - returns False or raise an error if data is empty, else returns True

    """
    
    # Check if dataframe is empty
    if df.empty:
        print("\nDataframe empty. Finishing execution")
        return False 

    # Check for nulls
    if df.name.empty:
        raise Exception("\nName is Null or the value is empty")
 
     # Check for nulls
    if df.category.empty:
        raise Exception("\nCategory is Null or the value is empty")

    # Check for nulls
    if df.price.empty:
        raise Exception("\nPrice is Null or the value is empty")

    return True


def connect_db():
    """Function to connect to database

    :return: obj - the connection object

    It connect to RDS database using the endpoint, the name of the created database, the default user and it's password.
    """
    # sets the system to use the user, the password and the jdbc url from the .env file
    dotenv.load_dotenv(dotenv.find_dotenv())
    password_rds = os.getenv("password_rds")


    con = psycopg2.connect(host='database-1.cuwe6gyvxfwp.us-west-2.rds.amazonaws.com', 
                           dbname='bookclub', 
                           user='postgres', 
                           password=password_rds,
                           port = 5432)
    return con


def create_table(sql):
    """Function that creates the table in the database

	:param sql: str query to be executed
	"""

    con = connect_db() 
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()


def insert_data(sql, values):
    """Function that inserts data into the database based on the SQL and the values given
    
    :param sql: str query to be executed
    :param values: tuple values to be inserted into the table

    """

    # validate data
    if check_if_valid_data(df_book_data):
        print("\nData valid, proceed to Load stage")
    # create connection object
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute(sql, values)
        print("Data was sucessfully loaded on database")
    except Exception as error:
        print(f"{values} were not loaded on database. Error: {error}")

    con.commit()
    con.close()


def consult_db(sql):
    """Function that gets data from the database using a sql query

    :param sql: str query to be executed
    :return: list - it contains all the desired data gathered from the database

    It connects to the database and returns all the desired data in a list
    """

    con = connect_db()
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    records = []
    for rec in recset:
        records.append(rec)
    con.close()
    return records

# defines an option to navigation
options = Options()

# it creates the browser object
browser = webdriver.Firefox(options=options)

# calls the functions to get all the books' data from the web
book_links = get_book_links(browser)
complete_book_data = get_book_data(browser, book_links)

# transform web data into a dataframe
df_book_data = pd.DataFrame(complete_book_data, columns=['name', 'category', 'stars', 'price', 'availability'])

# drops, if exists, and creates squence id and books table 
create_table("""DROP TABLE IF EXISTS books;""")
create_table("""DROP SEQUENCE id;""")
create_table("""CREATE SEQUENCE id;""")
create_table("""CREATE TABLE IF NOT EXISTS books 
                                    (id INT default nextval('id'::regclass) PRIMARY KEY, 
                                    name VARCHAR(250),
                                    category VARCHAR(20),
                                    stars VARCHAR(5),
                                    price FLOAT,
                                    availability VARCHAR(10));
                                    """) # pede para o cursor executar a query mencionada 

# gets the book data from the dataframe and inserts it into the desired table
for book in df_book_data.itertuples():
    if '%' in book.name:
        name = str(book.name).replace("%", "%%")
    else:
        name = str(book.name).replace("'", "''")
    category = str(book.category)
    stars = str(book.stars)
    price = float(book.price)
    availability = str(book.availability)

    print(f"{name}, {category}, {stars}, {price}, {availability}")


    sql = f"""INSERT INTO books (name, category, stars, price, availability)
               VALUES ('{name}', '{category}', '{stars}', '{price}', '{availability}')
                """
    
    values = (name, category, stars, price, availability)
    insert_data(sql, values)

# get and print all data from books table
records = consult_db('SELECT * FROM books;')
print(records)
