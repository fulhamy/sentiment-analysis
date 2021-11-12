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
        read_table = """select index, "Source", title, published_at date,body, "UID", published_by, body, id,subjectivity, polarity from news_log where subjectivity is null and polarity is null and length(body) > 20 order by id asc limit 1"""
        cur.execute(read_table)
        px_data = pd.read_sql_query(read_table, con)
        records = cur.fetchall()
        
        for row in records:
        
            body_text = TextBlob(row[5])
            polarity_score = body_text.sentiment.polarity
            subjectivity_score = body_text.sentiment.polarity
            id_number = row[9]

            cur.execute('''UPDATE news_log SET subjectivity = subjectivity_score, polarity = polarity_score WHERE id = id_number''')


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
