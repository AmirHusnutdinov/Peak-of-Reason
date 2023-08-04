import psycopg2
from flask import render_template
from Links import params
import math

from settings import host, user, password, db_name


class Blog:
    @staticmethod
    def blog():
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute('''SELECT id, photo_way, name,
                                        signature, link, created_date, post_text FROM blog;''')
                posts = cursor.fetchall()

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")

        three_posts = []

        start = 0
        end = 3
        blog_inform = posts[::-1]
        count_of_columns = math.ceil(len(blog_inform) / 3)
        count_of_posts = len(blog_inform)
        for i in range(count_of_columns):
            three_posts.append(blog_inform[start:end])

            if start + 3 <= count_of_posts:
                start += 3

            if end + 3 <= count_of_posts:
                end += 3

            elif end + 2 <= count_of_posts:
                end += 2

            elif end + 1 <= count_of_posts:
                end += 1

        return render_template('blog_page.html', **params, bl_is_active='active',
                               title='Blog page', posts=three_posts,
                               )

    @staticmethod
    def blog_pages(number):
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT version();"
                )

                print(f"Server version: {cursor.fetchone()}")

            with connection.cursor() as cursor:
                cursor.execute('''SELECT id, photo_way, name,
                                        signature, link, created_date, post_text FROM blog;''')
                posts = cursor.fetchall()

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        item = posts[number]
        return render_template('blog_page_example.html', **params,
                               bl_is_active='active',
                               name=item[2],
                               signature=item[3],
                               date=item[5],
                               photo_name=item[1],
                               text=item[6], title='Blog page')
