import psycopg2, os
import pandas as pd
from textblob import TextBlob

# read database connection url from the enivron variable we just set.
DATABASE_URL = os.environ.get('DATABASE_URL')

con = None

for i in range(0, 8343244, 1):

    iteration = i
    try:
        # create a new database connection by calling the connect() function
        con = psycopg2.connect(DATABASE_URL)

        #  create a new cursor
        cur = con.cursor()
        read_table = """select index, "Source", title, published_at,body, "UID", published_by, body, id,subjectivity, polarity from news_log where subjectivity is null and polarity is null and length(body) > 20 order by id asc limit 1"""
        cur.execute(read_table)
        df = pd.read_sql_query(read_table, con)
        px_data = pd.read_sql_query(read_table, con)
        df = df.set_index('date')
        data = df
        
        body_text = TextBlob(px_data.df['body'])
        
        body_text.sentiment.polarity
        
        cur.execute('''UPDATE news_log SET subjectivity = body_text.sentiment.subjectivity, polarity = body_text.sentiment.polarity WHERE id = px_data.df['id']''')
        
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
