import psycopg2
from flask import render_template, session, flash
from Links import params
from Reviews.reviewsform import ReviewsForm
from settings import host, user, password, db_name


class Reviews:
    @staticmethod
    def get_date(date):
        day_list = ['первое', 'второе', 'третье', 'четвёртое',
                    'пятое', 'шестое', 'седьмое', 'восьмое',
                    'девятое', 'десятое', 'одиннадцатое', 'двенадцатое',
                    'тринадцатое', 'четырнадцатое', 'пятнадцатое', 'шестнадцатое',
                    'семнадцатое', 'восемнадцатое', 'девятнадцатое', 'двадцатое',
                    'двадцать первое', 'двадцать второе', 'двадцать третье',
                    'двадцать четвёртое', 'двадцать пятое', 'двадцать шестое',
                    'двадцать седьмое', 'двадцать восьмое', 'двадцать девятое',
                    'тридцатое', 'тридцать первое']
        month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                      'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
        date_list = date.split('-')
        return (day_list[int(date_list[0]) - 1] + ' ' +
                month_list[int(date_list[1]) - 1] + ' ' +
                date_list[2] + ' года')

    @staticmethod
    def reviews():
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
                    """select users.name, estimation, comment, created_date, feedback.photo_way from feedback 
                    INNER JOIN users ON feedback.user_id = users.user_id
                    order by random() limit 4;"""
                )
                rand_list = cursor.fetchall()
            with connection.cursor() as cursor:
                cursor.execute('''SELECT to_char(current_date, 'dd-mm-yyyy');''')
                date = cursor.fetchone()[0]

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")

        form = ReviewsForm()
        if form.validate_on_submit():
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
                        f"""INSERT INTO feedback_to_moderate (user_id, estimation, comment, created_date) 
                            values
                            ((SELECT user_id FROM users WHERE user_id = {session.get("id")}::int), 
                            {int(form.prof.data)}, '{form.text.data}', '{date}'::date);"""
                    )

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")
            return '/reviews'

        return render_template('reviews_page.html',
                               **params,
                               reviews_=rand_list,
                               re_is_active='active', form=form,
                               title='Reviews', login=session.get('authorization')
                               )
