from flask import render_template, session
import math
from Links import types, params, event
from settings import host, user, password, db_name
import psycopg2


class Events:
    @staticmethod
    def events(events_lst, file):
        print(events_lst)
        event1 = event + '/?teen=1'
        event2 = event + '/?adult=1'
        if not file:
            return render_template('events.html', **params, ev_is_active='active',
                                   event1=event1,
                                   event2=event2,
                                   posts=events_lst, title='Events', login=session.get('authorization'))
        else:
            return render_template(file, **params, ev_is_active='active', title='Events',
                                   login=session.get('authorization'))

    @staticmethod
    def event(events1, mode):
        if mode == 'teen':
            print(events1)
            return render_template('event1.html', **params, ev_is_active='active',
                                   link1=(types + '/?ac=1'),
                                   link2=(types + '/?ay=1'),
                                   link3=(types + '/?ot=1'),
                                   posts=events1, title='Events',
                                   login=session.get('authorization'))

        elif mode == 'adult':
            return render_template('event2.html', **params, ev_is_active='active',
                                   link1=(types + '/?mt=1'),
                                   link2=(types + '/?oa=1'),
                                   posts=events1, title='Events',
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
