from settings import host, user, password, db_name
import psycopg2


def database_query(sql):
    connection = []
    try:
        connection = psycopg2.connect(
            host=host, user=user, password=password, database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")
