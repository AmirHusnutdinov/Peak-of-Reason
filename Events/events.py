from flask import render_template, session
from Links import params, event
from database_query import database_query
from Blog.blog import make_date


class Events:
    @staticmethod
    def events():
        events_lst = database_query(f"""SELECT id, photo_way, name, signature,
         link, to_char(created_date, 'dd Mon YYYY') FROM events
        ORDER BY created_date DESC; """)
        events_lst = list(map(list, events_lst))
        for i in range(len(events_lst)):
            events_lst[i][5] = make_date(events_lst[i][5])
        event1 = event + "/?teen=1"
        event2 = event + "/?adult=1"
        return render_template(
            "event/events.html",
            **params,
            ev_is_active="active",
            event1=event1,
            event2=event2,
            posts=events_lst,
            title="События",
            login=session.get("authorization"),
        )

    @staticmethod
    def filtering_events(query1, query2, query3, query4, query5, query6, query7):
        mode = ""
        label = ""
        event_info = ""
        if query1 and query1 != "":
            event_info = database_query("""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                            FROM events WHERE is_teen = 'true'::bool;""")
            mode = "teen"

        elif query2 and query2 != "":
            event_info = database_query("""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')   
                        FROM events WHERE is_adult = 'true'::bool;""")
            mode = "adult"

        if query3 and query3 != "":
            label = "Профилактика эмоционального выгорания через муз. терапию"
            event_info = database_query("""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                        FROM events WHERE is_poebtmt = 'true'::bool;""")
            mode = "mt"

        elif query4 and query4 != "":
            label = "«Харизматичный оратор» 18+"
            event_info = database_query(f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                        FROM events WHERE is_oratory_adult = 'true'::bool;""")
            mode = "oa"

        elif query5 and query5 != "":
            label = "«Искусство общения» 12-14"
            event_info = database_query("""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                        FROM events WHERE is_taoc = 'true'::bool;""")
            mode = "ac"

        elif query6 and query6 != "":
            label = "«Искусство быть собой» 14-16 лет"
            event_info = database_query("""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                        FROM events WHERE is_taoby = 'true'::bool;""")
            mode = "ay"

        elif query7 and query7 != "":
            label = "«Харизматичный оратор» 15-18"
            event_info = database_query("""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                        FROM events WHERE is_oratory_teen = 'true'::bool;""")
            mode = "ot"
        date = event_info[0][5]
        date = make_date(date)

        if mode == "teen":
            return render_template(
                "event/event1.html",
                **params,
                ev_is_active="active",
                link1=(event + "/?ac=1"),
                link2=(event + "/?ay=1"),
                link3=(event + "/?ot=1"),
                date=date,
                posts=event_info,
                title="События для подростков",
            )

        elif mode == "adult":
            return render_template(
                "event/event2.html",
                **params,
                ev_is_active="active",
                link1=(event + "/?mt=1"),
                link2=(event + "/?oa=1"),
                date=date,
                posts=event_info,
                title="События для взрослых",
            )

        else:
            if mode in ["ac", "ay", "ot"]:
                back_link = event + "/?teen=1"
            elif mode in ["mt", "oa"]:
                back_link = event + "/?adult=1"
            else:
                back_link = "/"

            return render_template(
                "event/event3.html",
                **params,
                ev_is_active="active",
                label=label,
                back_link=back_link,
                posts=event_info,
                title="События",
                date=date,
                login=session.get("authorization"),
            )

    @staticmethod
    def event_pages(number):
        posts = database_query( f"""SELECT id, photo_way, name,
                                        signature, link, created_date, post_text,
                                         time, count_of_people, id_of_people, price FROM events 
                                        where id = {number};""")
        item = posts[0]
        date = ".".join(str(item[5]).split("-")[::-1])
        time = ":".join((item[7].split(":"))[:2])
        last_places = item[8] - len(item[9])
        flag_confirm = False
        if last_places <= 0:
            flag_confirm = True
        flag = True
        if session.get("authorization"):
            if int(session.get("id")) in item[9]:
                flag = False
        return render_template(
            "event/event_page_example.html",
            **params,
            ev_is_active="active",
            name=item[2],
            signature=item[3],
            date_show=date,
            date=item[5],
            photo_name=item[1],
            text=item[6],
            time=time,
            flag=flag,
            count_of_people=item[8],
            number=number,
            flag_confirm=flag_confirm,
            last_places=last_places,
            price=item[10],
            title="События",
            login=session.get("authorization"),
        )

    @staticmethod
    def event_buy_pages(page):
        posts = database_query(f"""SELECT count_of_people, id_of_people FROM events 
                                                    where id = {page};""")
        item = posts[0]
        last_places = item[0] - len(item[1])
        if last_places > 0:
            posts = database_query(f"""SELECT id, photo_way, name,
                                            signature, created_date, time FROM events 
                                            where id = {page};""")
            item = posts[0]
            date = ".".join(str(item[4]).split("-")[::-1])
            time = ":".join((item[5].split(":"))[:2])
            print(item[1])
            return render_template(
                "event/buy_page_example.html",
                **params,
                ev_is_active="active",
                id=page,
                name=item[2],
                signature=item[3],
                date_show=date,
                photo_name=item[1],
                time=time,
                title="Подтверждение регистрации на событие",
                login=session.get("authorization"),
            )
        else:
            return False

    @staticmethod
    def event_confirm(event_id, user_id):

        posts = database_query(f"""SELECT count_of_people, id_of_people FROM events 
                                                    where id = {event_id};""")
        item = posts[0]
        last_places = item[0] - len(item[1])
        if last_places > 0:
            info_about_people = database_query(f"""SELECT count_of_people, id_of_people FROM events 
                                            where id = {event_id};""")
            if (int(info_about_people[0][0]) != len(info_about_people[0][1])
                    and int(session.get("id")) not in info_about_people[0][1]):
                database_query(f"""Update events 
                                Set id_of_people = array_append(id_of_people, {user_id})
                                WHERE id = '{event_id}'""")

                database_query(f"""Update users 
                                Set id_of_event = array_append(id_of_event, {event_id})
                                WHERE user_id = '{user_id}'""")
                return True
        return False
