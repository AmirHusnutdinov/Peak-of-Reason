from flask import render_template, session
import math
from Links import types, params, event
from settings import host, user, password, db_name
import psycopg2


class Events:
    @staticmethod
    def three_posts_funk(events_lst):
        count_of_columns = math.ceil(len(events_lst) / 3)
        count_of_posts = len(events_lst)

        three_posts = []

        start = 0
        end = 3
        event_inform = events_lst[::-1]
        for i in range(count_of_columns):
            three_posts.append(event_inform[start:end])

            if start + 3 <= count_of_posts:
                start += 3

            if end + 3 <= count_of_posts:
                end += 3

            elif end + 2 <= count_of_posts:
                end += 2

            elif end + 1 <= count_of_posts:
                end += 1
        return three_posts

    @staticmethod
    def events(events_lst, file):
        three_posts = Events.three_posts_funk(events_lst)
        event1 = event + '/?teen=1'
        event2 = event + '/?adult=1'
        if not file:
            return render_template('events.html', **params, ev_is_active='active',
                                   event1=event1,
                                   event2=event2,
                                   posts=three_posts, title='Events', login=session.get('authorization'))
        else:
            return render_template(file, **params, ev_is_active='active', title='Events',
                                   login=session.get('authorization'))

    @staticmethod
    def event(events1, mode):
        three_posts = Events.three_posts_funk(events1)
        pb = ''
        tt = ''
        orator = ''
        file = ''

        if mode == 'teen':
            pb = types + '/?pb=1'
            tt = types + '/?tt=1'
            orator = types + '/?orator=1'
            file = 'event1.html'

        elif mode == 'adult':
            pb = types + '/?tp=1'
            tt = types + '/?ic=1'
            orator = types + '/?ac=1'
            file = 'event2.html'

        return render_template(file, **params, ev_is_active='active',
                               pb=pb,
                               tt=tt,
                               orator=orator,
                               posts=three_posts, title='Events',
                               login=session.get('authorization'))

    @staticmethod
    def types_of_events(events_type, label):
        three_posts = Events.three_posts_funk(events_type)
        return render_template('types.html',
                               **params, ev_is_active='active',
                               posts=three_posts,
                               label=label, title='Events',
                               login=session.get('authorization')
                               )

    @staticmethod
    def event_pages(number):
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
                                            signature, link, created_date FROM events;''')
                posts = cursor.fetchall()

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        item = posts[number]
        return render_template('blog_page_example.html', **params,
                               ev_is_active='active',
                               name=item[2],
                               signature=item[3],
                               date=item[5],
                               photo_name=item[1],
                               text=item[6], title='Event page', login=session.get('authorization'))
