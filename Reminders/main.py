import schedule
from settings import app, host, user, password, db_name
import psycopg2
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


def send_email(id_human, mode):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT email FROM users WHERE user_id = {id_human} ''')

            human_info = cursor.fetchall()
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

    sender = "amirhusnutdinov800900@gmail.com"
    password_email = 'smta gzvy aonh dccg'

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        with open("../templates/email_template.html") as file:
            template = file.read()
    except IOError:
        return "The template file doesn't found!"

    try:
        server.login(sender, password_email)
        msg = MIMEText(template, "html")
        msg["From"] = sender
        msg["To"] = human_info[0]
        if mode == 'day':
            msg["Subject"] = "Напоминаем меньше чем через сутки начинается занятие!"
        elif mode == 'hour':
            msg["Subject"] = "Напоминаем меньше чем через два часа начинается занятие!"
        server.sendmail(sender, human_info[0], msg.as_string())

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


def greeting():
    today = datetime.now()
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT id, created_date, time, id_of_people, notified FROM events''')

            event_info = cursor.fetchall()
        for event in event_info:
            print(event)
            datetime_of_event = datetime.strptime(f'{event[1]} {event[2].strip()}', '%Y-%m-%d %H:%M:%S')

            people = event[3]
            notified = event[4]
            workable_date = datetime_of_event - today
            print((str(workable_date)))

            if int(str(workable_date).split()[0]) < 1 and not notified:
                print('ABOBA')
                mode = 'day'
                for id_human in people:
                    send_email(id_human, mode)
                with connection.cursor() as cursor:
                    cursor.execute(f"""Update events 
                                Set notified = True
                                WHERE id = '{event[0]}' """)

            elif int(str(workable_date).split()[0]) < -1:
                with connection.cursor() as cursor:
                    cursor.execute(f"""Delete from events 
                                WHERE id = '{event[0]}' """)

            else:
                print('good')
            # elif notified and int(str(workable_date).split()[1]):
            #     mode = 'hour'
            #     for id_human in people:
            #         send_email(id_human, mode)
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)

    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def main():
    schedule.every(5).seconds.do(greeting)
    schedule.every().hour.do(greeting)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
