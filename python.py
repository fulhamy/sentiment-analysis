import psycopg2, os
import pandas as pd
from textblob import TextBlob

# read database connection url from the enivron variable we just set.
DATABASE_URL = os.environ.get('DATABASE_URL')

con = None

try:
    # create a new database connection by calling the connect() function
    con = psycopg2.connect(DATABASE_URL)

    #  create a new cursor
    cur = con.cursor()
    read_table = """SELECT date_trunc('year', date) as date, sum(articles) as articles from mymatview2 group by 1 order by 1"""
    cur.execute(read_table)
    df = pd.read_sql_query(read_table, con)
    px_data = pd.read_sql_query(read_table, con)
    df = df.set_index('date')
    data = df
    total_articles = int(df['articles'].sum())
    cur.fetchall()
    print(cur.fetchall())
    print(data)
     # close the communication with the HerokuPostgres
    cur.close()
except Exception as error:
    print('Could not connect to the Database.')
    print('Cause: {}'.format(error))

finally:
    # close the communication with the database server by calling the close()
    if con is not None:
        con.close()
        print('Database connection closed.')
