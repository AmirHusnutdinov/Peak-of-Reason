from flask import render_template, session
from Links import types, params, event, events
from settings import host, user, password, db_name
import psycopg2


class Events:
    @staticmethod
    def events(events_lst):
        event1 = event + '/?teen=1'
        event2 = event + '/?adult=1'
        return render_template('events.html', **params, ev_is_active='active',
                               event1=event1,
                               event2=event2,
                               posts=events_lst, title='Events', login=session.get('authorization'))

    @staticmethod
    def event(events1, mode, label):
        if mode == 'teen':
            return render_template('event1.html', **params, ev_is_active='active',
                                   link1=(event + '/?ac=1'),
                                   link2=(event + '/?ay=1'),
                                   link3=(event + '/?ot=1'),
                                   # back_link=f'{event + "/"}',
                                   posts=events1, title='Events',
                                   login=session.get('authorization'))

        elif mode == 'adult':
            return render_template('event2.html', **params, ev_is_active='active',
                                   link1=(event + '/?mt=1'),
                                   link2=(event + '/?oa=1'),
                                   # back_link=f'{event}',
                                   posts=events1, title='Events',
                                   login=session.get('authorization'))

        else:
            if mode in ['ac', 'ay', 'ot']:
                back_link = event + '/?teen=1'
            elif mode in ['mt', 'oa']:
                back_link = event + '/?adult=1'
            else:
                back_link = '/'

            return render_template('event3.html', **params, ev_is_active='active',
                                   label=label, back_link=back_link,
                                   posts=events1, title='Events',
                                   login=session.get('authorization'))

    @staticmethod
    def types_of_events(events_type, label):
        return render_template('types.html',
                               **params, ev_is_active='active',
                               label=label, title='Events', posts=events_type,
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
                cursor.execute(f'''SELECT id, photo_way, name,
                                        signature, link, created_date, post_text, time FROM events 
                                        where id = {number};''')
                posts = cursor.fetchall()
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        item = posts[0]
        return render_template('event_page_example.html', **params,
                               ev_is_active='active',
                               name=item[2],
                               signature=item[3],
                               date=item[5],
                               photo_name=item[1],
                               text=item[6],
                               time=item[7], title='event', login=session.get('authorization'))
