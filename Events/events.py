from flask import render_template, session
from Links import params, event
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
                                        signature, link, created_date, post_text, time, count_of_people FROM events 
                                        where id = {number};''')
                posts = cursor.fetchall()
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        item = posts[0]
        date = '.'.join(str(item[5]).split('-')[::-1])
        time = ':'.join((item[7].split(':'))[:2])
        return render_template('event_page_example.html', **params,
                               ev_is_active='active',
                               name=item[2],
                               signature=item[3],
                               date_show=date,
                               date=item[5],
                               photo_name=item[1],
                               text=item[6],
                               time=time,
                               count_of_people=item[8],
                               number=number,
                               title='event', login=session.get('authorization'))

    @staticmethod
    def event_buy_pages(number):
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
                                        signature, created_date, time FROM events 
                                        where id = {number};''')
                posts = cursor.fetchall()
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        item = posts[0]
        date = '.'.join(str(item[4]).split('-')[::-1])
        time = ':'.join((item[5].split(':'))[:2])
        return render_template('buy_page_example.html', **params,
                               ev_is_active='active',
                               id=number,
                               name=item[2],
                               signature=item[3],
                               date_show=date,
                               photo_name=item[1],
                               time=time,
                               title='event', login=session.get('authorization'))

    @staticmethod
    def event_confirm(event_id, user_id):
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(f'''SELECT count_of_people, id_of_people FROM events 
                                        where id = {event_id};''')

                info_about_people = cursor.fetchall()
                if int(info_about_people[0][0]) != len(info_about_people[0][1]):
                    with connection.cursor() as cursor:
                        cursor.execute(f"""Update events 
                                    Set id_of_people = array_append(id_of_people, {user_id})
                                    WHERE id = '{event_id}' """)

                    with connection.cursor() as cursor:
                        cursor.execute(f"""Update users 
                                    Set id_of_event = array_append(id_of_event, {event_id})
                                    WHERE user_id = '{user_id}'""")

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
