import schedule
from settings import host, user, password, db_name
import psycopg2
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


def send_email(id_human, mode, event_name, event_date, event_time):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT email, name,  FROM users WHERE user_id = {id_human} INNER JOIN events.''')

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

    template = '''
                <!DOCTYPE html>
                <html amp4email>
                <head>
                    <meta name="viewport" content="width=device-width" />
                    <meta name="robots" content="noindex, nofollow">
                    <script>
                    window.onload = function() {
                        const a = window.location.hash;
                        if(a.startsWith('#googleCalendarWidget'))
                        {
                            const btnElement = document.getElementById('add-to-calendar-btn');
                            if(btnElement) btnElement.click();
                        }
                    };
                    </script>
                    <meta charset="utf-8">
                    <script async src="https://cdn.ampproject.org/v0.js"></script>
                    <style amp4email-boilerplate>body{visibility:hidden}</style>
                    <style amp-custom>@media only screen and (min-width:480px){.mj-column-per-100{width:100%;max-width:100%}}@media only screen and (max-width:480px){table.mj-full-width-mobile{width:100%}td.mj-full-width-mobile{width:auto}}div p{margin:0 0}h1,h2,h3,h4,h5,h6{margin:0}h1{font-size:28px}h2{font-size:24px}h3{font-size:20px}h4{font-size:18px}p{font-size:16px}.form-text h1,.form-text h2,.form-text h3,.form-text h4,.form-text p{color:revert;font-size:revert;font-family:inherit}.question h1,.question h2,.question h3,.question h4,.question p{color:revert;font-size:revert;font-family:inherit}@media (max-width:480px){h1{font-size:28px}h2{font-size:24px}h3{font-size:20px}h4{font-size:18px}p{font-size:16px}}.amp-html-block p{font-size:inherit;color:revert}.amp-btn-wrapper p{font-size:inherit;color:revert}a{text-decoration:none}ol,ul{margin-top:0;margin-bottom:0;list-style-position:inside;padding-inline-start:0;padding-left:0}figure.table{margin:0}figure.table table{width:100%}figure.table table td,figure.table table th{min-width:2em;padding:.4em;border:1px solid #bfbfbf}.hide-on-desktop{display:none}@media screen and (max-width:480px){.hide-on-desktop{display:revert}.hide-on-mobile{display:none}.mj-column-per-33{padding:4px 0 4px 0}.mj-sa-column-per-10{width:15%}.mj-sa-column-per-70{width:65%}}body{margin:0;padding:0}table,td{border-collapse:collapse}img{border:0;height:auto;line-height:100%;outline:0}p{display:block;margin:13px 0}</style>
                </head>
                <body style="word-spacing:normal;background-color:#f8fafc">
                <span style="display:none">Explore interactive templates by Mailmodo</span>
                <div style="background-color:#f8fafc">
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" >
                        <tr>
                            <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                                <div style="background:#fff;background-color:#fff;margin:0 auto;max-width:600px">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#fff;background-color:#fff;width:100%">
                                        <tbody>
                                        <tr>
                                            <td style="direction:ltr;font-size:0;padding:0;padding-bottom:0;padding-left:0;padding-right:0;padding-top:0;text-align:center">
                                                <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                                    <tr>
                                                        <td class="" width="600px" >
                                                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" >
                                                                <tr>
                                                                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                                                                        <div style="background:#fff;background-color:#fff;margin:0 auto;max-width:600px">
                                                                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#fff;background-color:#fff;width:100%">
                                                                                <tbody>
                                                                                <tr>
                                                                                    <td style="border:0 solid #1e293b;direction:ltr;font-size:0;padding-bottom:16px;padding-left:16px;padding-right:16px;padding-top:16px;text-align:center">
                                                                                        <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                                                                            <tr>
                                                                                                <td class="" style="vertical-align:top;width:568px;" >
                                                                                                    <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">
                                                                                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                                                                                            <tbody>
                                                                                                            <tr>
                                                                                                                <td style="background-color:transparent;border:0 solid transparent;vertical-align:top;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0">
                                                                                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                                                                                                        <tbody>
                                                                                                                        <tr>
                                                                                                                            <td align="center" style="font-size:0;padding:0;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;word-break:break-word">
                                                                                                                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0" class="mj-full-width-mobile">
                                                                                                                                    <tbody>
                                                                                                                                    <tr>
                                                                                                                                        <td style="width:289px" class="mj-full-width-mobile">
                                                                                                                                            <amp-img alt="Alternate image text" src="./static/assets/images/logo1.jpeg" style="border:0 solid #1e293b;border-radius:0;display:block;outline:0;text-decoration:none;width:100%;font-size:13px" width="1000" height="800" layout="responsive"></amp-img>
                                                                                                                                        </td>
                                                                                                                                    </tr>
                                                                                                                                    </tbody>
                                                                                                                                </table>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        </tbody>
                                                                                                                    </table>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </div>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td class="" width="600px" >
                                                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" >
                                                                <tr>
                                                                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                                                                        <div style="background:#fff;background-color:#fff;margin:0 auto;max-width:600px">
                                                                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#fff;background-color:#fff;width:100%">
                                                                                <tbody>
                                                                                <tr>
                                                                                    <td style="border:0 solid transparent;direction:ltr;font-size:0;padding-bottom:30px;padding-left:30px;padding-right:30px;padding-top:30px;text-align:center">
                                                                                        <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                                                                            <tr>
                                                                                                <td class="" style="vertical-align:top;width:540px;" >
                                                                                                    <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">
                                                                                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="background-color:transparent;border:0 solid transparent;vertical-align:top" width="100%">
                                                                                                            <tbody>
                                                                                                            <tr>
                                                                                                                <td align="left" style="font-size:0;padding:10px 25px;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;word-break:break-word">
                                                                                                                    <div style="font-family:Helvetica;font-size:32px;font-weight:700;letter-spacing:0;line-height:1.5;text-align:left;color:#334155">
                                                                                                                        <p style="text-align:center">Уведомление о записи на событие</p>
                                                                                                                    </div>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr>
                                                                                                                <td align="left" style="font-size:0;padding:10px 25px;padding-top:0;padding-right:0;padding-bottom:24px;padding-left:0;word-break:break-word">
                                                                                                                    <div style="font-family:Helvetica;font-size:16px;font-weight:400;letter-spacing:0;line-height:1.5;text-align:left;color:#475569">
                                                                                                                        <p style="text-align:justify">&#xA0;</p>
                                                                                                                        <p style="text-align:justify">
                                                                                                                            <span style="font-size:16px">Здравствуйте''', human_info[1], '''! Вы записались на ''', event_name, ''' в ''', event_date, event_time + '''.</span>
                                                                                                                        </p>
                                                                                                                        <p style="text-align:justify">
                                                                                                                            <span style="font-size:16px">Помните: Если вы записались и при этом не пришли на занятие, не предупредив организаторов, вам будет выдана блокировка.</span>
                                                                                                                        </p>
                                                                                                                    </div>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr>
                                                                                                                <td align="center" class="amp-btn-wrapper" style="font-size:0;padding:12px 0 12px 0;word-break:break-word">
                                                                                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate;width:auto;line-height:100%">
                                                                                                                        <tbody>
                                                                                                                        <tr>
                                                                                                                            <td align="center" bgcolor="#1E293B" role="presentation" style="border-radius:4px;border:0 solid none;cursor:auto;height:auto;background:#1e293b;padding:0">
                                                                                                                                <a href="some_link" style="display:inline-block;background:#1e293b;color:#fff;font-family:Helvetica;font-size:16px;font-weight:400;line-height:1;letter-spacing:1px;margin:0;text-decoration:none;text-transform:none;padding:12px 24px 12px 24px;border-radius:4px" target="_blank" data-block-id="block2eve656" data-block-type="block" data-url-id="dacc0710-55a8-5092-ab24-11a0937fe0d4">Узнать Больше</a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        </tbody>
                                                                                                                    </table>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </div>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td class="" width="600px" >
                                                            <table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" >
                                                                <tr>
                                                                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                                                                        <div style="background:#fff;background-color:#fff;margin:0 auto;max-width:600px">
                                                                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#fff;background-color:#fff;width:100%">
                                                                                <tbody>
                                                                                <tr>
                                                                                    <td style="border:0 solid #1e293b;direction:ltr;font-size:0;padding-bottom:16px;padding-left:16px;padding-right:16px;padding-top:16px;text-align:center">
                                                                                        <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                                                                            <tr>
                                                                                                <td class="" style="vertical-align:top;width:568px;" >
                                                                                                    <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">
                                                                                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                                                                                            <tbody>
                                                                                                            <tr>
                                                                                                                <td style="background-color:transparent;border:0 solid transparent;vertical-align:top;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0">
                                                                                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                                                                                                        <tbody>
                                                                                                                        <tr>
                                                                                                                            <td align="center" style="font-size:0;padding:10px 25px;padding-top:12px;padding-right:0;padding-bottom:12px;padding-left:0;word-break:break-word">
                                                                                                                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" >
                                                                                                                                </table>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        </tbody>
                                                                                                                    </table>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </div>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </td>
                        </tr>
                    </table>
                </div>
                <amp-img width="1" height="1" alt="signature" src="https://t.mmtrkr.com/opens/web/637d63e7-1851-5eda-ba6b-28701f1c1845/sampleRecipientIdFromWebsite"></amp-img>
                <table width="100%" align="center" style="font-family:&apos;arial&apos;;max-width:600px;margin:0 auto;margin-top:12px;">
                </table>
                </body>
                </html> 
    '''

    try:
        server.login(sender, password_email)
        msg = MIMEText(template, "html")
        msg["From"] = sender
        msg["To"] = human_info[0][0]
        if mode == 'day':
            msg["Subject"] = "Напоминаем меньше чем через сутки начинается занятие!"
        elif mode == 'hour':
            msg["Subject"] = "Напоминаем меньше чем через два часа начинается занятие!"
        server.sendmail(sender, human_info[0][0], msg.as_string())

        print("The message was sent successfully!")
    except Exception as _ex:
        print(f"{_ex}\nCheck your login or password please!")


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
            cursor.execute(f'''SELECT id, created_date, time, id_of_people, notified, name FROM events''')

            event_info = cursor.fetchall()
        for event in event_info:
            print(event)
            datetime_of_event = datetime.strptime(f'{event[1]} {event[2].strip()}', '%Y-%m-%d %H:%M:%S')

            people = event[3]
            notified = event[4]
            workable_date = datetime_of_event - today

            if len((str(workable_date)).split(',')) == 1:
                if int((str(workable_date)).split(':')[0]) > 1 and not notified:
                    mode = 'day'
                    for id_human in people:
                        send_email(id_human, mode)
                    with connection.cursor() as cursor:
                        cursor.execute(f"""Update events 
                                    Set notified = True
                                    WHERE id = '{event[0]}' """)

                elif notified and int((str(workable_date)).split(':')[0]) == 1:
                    mode = 'hour'
                    for id_human in people:
                        send_email(id_human, mode, event[5], event[1], event[2])

            elif int(str(workable_date).split()[0]) < -1:
                with connection.cursor() as cursor:
                    cursor.execute(f"""Delete from events 
                                WHERE id = '{event[0]}' """)

            else:
                print('good')

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)

    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def main():
    # schedule.every(5).seconds.do(greeting)
    schedule.every().hour.do(greeting)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
