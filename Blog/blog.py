import psycopg2
from flask import render_template, session
from Links import params
import math
from Blog.blog_form import BlogForm

from settings import host, user, password, db_name


def make_date(date):
    date = date.split()
    months = {
        "Sep": "Сентября",
        "Oct": "Октября",
        "Nov": "Ноября",
        "Dec": "Декабря",
        "Jan": "Января",
        "Feb": "Февраля",
        "Mar": "Марта",
        "Apr": "Апреля",
        "May": "Мая",
        "Jun": "Июня",
        "Jul": "Июля",
        "Aug": "Августа",
    }
    for i, month in enumerate(months):
        if date[1] == month:
            date[1] = list(months.values())[i]
            if date[0][0] == "0":
                date[0] = date[0][1]
            date = " ".join(date)
    return date


def fucking_date(lst):
    months = {
        "Sep": "Сентября",
        "Oct": "Октября",
        "Nov": "Ноября",
        "Dec": "Декабря",
        "Jan": "Января",
        "Feb": "Февраля",
        "Mar": "Марта",
        "Apr": "Апреля",
        "May": "Мая",
        "Jun": "Июня",
        "Jul": "Июля",
        "Aug": "Августа",
    }
    lst2 = []
    for item in lst:
        item = list(item)
        date = item[5].split()
        for i, month in enumerate(months):
            if date[1] == month:
                date[1] = list(months.values())[i]
                if date[0][0] == "0":
                    date[0] = date[0][1]
                date = " ".join(date)
                item[5] = date
        lst2.append(item)
    return lst2


class Blog:
    @staticmethod
    def blog():
        try:
            connection = psycopg2.connect(
                host=host, user=user, password=password, database=db_name
            )
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT id, photo_way, name,
                                        signature, link, to_char(created_date, 'dd Mon YYYY'), post_text FROM blog;"""
                )
                posts = cursor.fetchall()
                # for i in posts:
                #     s = str(list(i)[1]).replace(' ', '_')
                #     s = s.replace('.jpg_', '.jpg ')
                #     s = s[1:]
                #     cursor.execute(f"""
                #         UPDATE blog SET photo_way = '{s}' WHERE id = {i[0]}""")

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")

        posts = fucking_date(posts)
        three_posts = []
        start = 0
        end = 3
        blog_inform = posts[::-1]
        count_of_columns = math.ceil(len(blog_inform) / 3)
        count_of_posts = len(blog_inform)
        for i in range(len(blog_inform)):
            if len(blog_inform[i][3]) > 143:
                blog_inform[i][3] = blog_inform[i][3][:143] + '...'
            blog_inform[i][1] = blog_inform[i][1].split()[0]
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

        if session.get("admin"):  # Это нужно чтобы кнопка изменения поста была только у админов
            is_admin = True
        else:
            is_admin = False
        from Blog.blog_form import BlogForm
        form = BlogForm()
        return render_template(
            "blog_page.html",
            **params,
            bl_is_active="active",
            title="Блог",
            posts=three_posts,
            login=session.get("authorization"),
            is_admin=is_admin,
            form=form
        )

    @staticmethod
    def blog_pages(number):
        try:
            connection = psycopg2.connect(
                host=host, user=user, password=password, database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name,
                                        signature, link, to_char(created_date, 'dd Mon YYYY'), post_text FROM blog 
                                        where id = {number}
                                        ORDER BY created_date DESC;"""
                )
                posts = cursor.fetchall()
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        item = posts[0]
        date = make_date(item[5])
        print(item[1])
        return render_template(
            "blog_page_example.html",
            **params,
            bl_is_active="active",
            name=item[2],
            signature=item[3],
            date=date,
            photo_name=item[1],
            text=item[6],
            title="Блог",
            login=session.get("authorization"),
        )

    @staticmethod
    def delete_blog():
        form = BlogForm()
        if form.validate_on_submit():
            try:
                connection = psycopg2.connect(
                    host=host, user=user, password=password, database=db_name
                )
                connection.autocommit = True
                string = str(form.ids_to_delete).split()[-1]
                start = string.find('"')
                stop = string.rfind('"')
                lst = string[start+1:stop].split(',')
                for i in lst:
                    with connection.cursor() as cursor:
                        cursor.execute(f"""Delete from blog where id = {i} """)
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")
