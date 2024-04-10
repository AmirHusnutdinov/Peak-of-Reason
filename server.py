import psycopg2
import smtplib
from email.mime.text import MIMEText
from flask import session, render_template
from Links import params_admin, params, general
from Admin.file_adminform import FileForm
from Authorization.cabinet import CabinetPage

from Start_page.start_page import StartPage

from Reviews.reviews import Reviews

from Events.events import Events
from Events.data import event_api

from Blog.blog import Blog

from Answers.answers import Answers

from Admin.admin import Admin
from Authorization.account import Account
from settings import app, host, user, password, db_name

import os
from flask import flash, request, redirect
from werkzeug.utils import secure_filename
from Admin.generate_textform import GeneratePageForm

app = app
UPLOAD_FOLDER = "/path/to/the/uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def open_main():
    return StartPage.main()


@app.route("/reviews", methods=["GET", "POST"])
def open_reviews():
    info = Reviews.reviews()
    if request.method == "GET":
        return info
    elif request.method == "POST":
        return redirect(info)


@app.route("/events/")
def open_events():
    connection = []
    try:
        connection = psycopg2.connect(
            host=host, user=user, password=password, database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                FROM events
                ORDER BY created_date DESC; """
            )
            event_info = cursor.fetchall()
        return Events.events(event_info)
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


@app.route("/event/")
def open_event1():
    connection, mode, label = [], [], []
    try:
        connection = psycopg2.connect(
            host=host, user=user, password=password, database=db_name
        )
        connection.autocommit = True

        query1 = request.args.get("teen")
        query2 = request.args.get("adult")
        query3 = request.args.get("mt")
        query4 = request.args.get("oa")
        query5 = request.args.get("ac")
        query6 = request.args.get("ay")
        query7 = request.args.get("ot")
        mode = ""
        label = ""
        if query1 and query1 != "":
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_teen = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            mode = "teen"

        elif query2 and query2 != "":
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')   
                    FROM events WHERE is_adult = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            mode = "adult"

        if query3 and query3 != "":
            label = "Профилактика эмоционального выгорания через муз. терапию"
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_poebtmt = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            mode = "mt"

        elif query4 and query4 != "":
            label = "«Харизматичный оратор» 18+"
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_oratory_adult = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            mode = "oa"

        elif query5 and query5 != "":
            label = "«Искусство общения» 12-14"
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_taoc = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            mode = "ac"

        elif query6 and query6 != "":
            label = "«Искусство быть собой» 14-16 лет"
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_taoby = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            mode = "ay"

        elif query7 and query7 != "":
            label = "«Харизматичный оратор» 15-18"
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_oratory_teen = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            mode = "ot"

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")
    return Events.event(event_info, mode, label)


@app.route("/event/types/")
def open_event_type():
    page = request.args.get("page")
    if page and page != "":
        return Events.event_pages(int(page))
    return redirect("/")


@app.route("/event/buy/")
def open_buy_page():
    if session.get("authorization"):
        page = request.args.get("page")
        if page and page != "":
            try:
                connection = psycopg2.connect(
                    host=host, user=user, password=password, database=db_name
                )
                connection.autocommit = True
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""SELECT count_of_people, id_of_people FROM events 
                                            where id = {page};"""
                    )
                    posts = cursor.fetchall()
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")
            item = posts[0]
            last_places = item[0] - len(item[1])
            if last_places > 0:
                return Events.event_buy_pages(int(page))
            return redirect("/")
        return redirect("/")
    else:
        return redirect("/authorization")


@app.route("/event/buy/confirm/")
def confirm():
    if session.get("authorization"):
        event = int(request.args.get("page"))
        user_id = int(session.get("id"))
        if event and event != "":
            try:
                connection = psycopg2.connect(
                    host=host, user=user, password=password, database=db_name
                )
                connection.autocommit = True
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""SELECT count_of_people, id_of_people FROM events 
                                            where id = {event};"""
                    )
                    posts = cursor.fetchall()
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")
            item = posts[0]
            last_places = item[0] - len(item[1])
            if last_places > 0:
                Events.event_confirm(event, user_id)
                return redirect(f"/event/buy/?page={int(event)}")
            return redirect("/")
        return redirect("/")
    else:
        return redirect("/authorization")


@app.route("/blog/", methods=["GET", "POST"])
def open_blog():
    if session.get('admin'):
        if request.method == "POST":
            Blog.delete_blog()
            return redirect('/blog')

    query = request.args.get("page")
    if query and query != "":
        return Blog.blog_pages(int(query))

    return Blog.blog()


@app.route("/authorization", methods=["GET", "POST"])
def open_authorization():
    if not session.get("authorization"):
        info = Account.account_login()
        if request.method == "GET":
            return info
        elif request.method == "POST":
            return redirect(info)
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def open_register():
    if not session.get("authorization"):
        info = Account.account_register()
        if request.method == "GET":
            return info
        elif request.method == "POST":
            return redirect(info)
    else:
        return redirect("/")


@app.route("/cabinet", methods=["GET", "POST"])
def open_cabinet():
    if session.get("authorization"):
        info = CabinetPage.account_cabinet()
        if request.method == "GET":
            return info
        elif request.method == "POST":
            return redirect(info)
    else:
        return redirect("/authorization")


@app.route("/cabinet/logout")
def open_cabinet_logout():
    if session.get("authorization"):
        session.permanent = False
        session.pop("authorization", None)
        session.pop("id", None)
        session.pop("admin", None)
        return redirect("/")
    else:
        return redirect("/authorization")


@app.route("/cabinet/delete", methods=["GET", "POST"])
def open_cabinet_delete():
    if session.get("authorization"):
        if request.method == "GET":
            CabinetPage.account_cabinet_del()
            session.permanent = False
            session.pop("authorization", None)
            session.pop("id", None)
            session.pop("admin", None)
            return redirect("/")
    else:
        return redirect("/authorization")


@app.route("/answers", methods=["GET", "POST"])
def open_answers():
    info = Answers.answers()
    if request.method == "GET":
        return info
    elif request.method == "POST":
        return redirect(info)


@app.route("/blog_admin", methods=["POST", "GET"])
def open_admin():
    if session.get("admin"):
        info = Admin.admin()
        if request.method == "GET":
            return info
        elif request.method == "POST":
            return redirect(info)
    else:
        return redirect("/")


@app.route("/answers_admin", methods=["GET", "POST"])
def open_admin_answers():
    if session.get("admin"):
        info = Admin.admin_answers(request.method)
        if request.method == "GET":
            return info
        elif request.method == "POST":
            return redirect(info)
    else:
        return redirect("/")


@app.route("/reviews_admin", methods=["GET", "POST"])
def open_reviews_admin():
    if session.get("admin"):
        info = Admin.admin_rev(request.method)
        if request.method == "GET":
            return info
        elif request.method == "POST":
            return redirect(info)
    else:
        return redirect("/")


def allowed_file(filename):
    """Функция проверки расширения файла"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/add_photo_admin", methods=["GET", "POST"])
def open_add_photo():
    form = FileForm()
    if request.method == "GET":
        return render_template(
            "add_new_image.html",
            **params_admin,
            ph_is="active",
            form=form,
            title="Добавление нового изображения",
        )
    if request.method == "POST":
        if "file" not in request.files:
            flash("Не могу прочитать файл")
            return redirect(request.url)
        file = request.files["file"]

        if file.filename == "":
            flash("Нет выбранного файла")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(
                os.path.join(
                    f'static/assets/images/{request.form["teamDropdown"]}', filename
                )
            )

            return render_template(
                "add_new_image.html",
                **params_admin,
                ph_is="active",
                form=form,
                title="Добавление нового изображения",
            )


@app.route("/event_admin", methods=["GET", "POST"])
def open_event_admin():
    if session.get("admin"):
        info = Admin.event_admin()
        if request.method == "GET":
            return info
        elif request.method == "POST":
            return redirect(info)
    else:
        return redirect("/")


@app.route("/add_feedback/", methods=["GET"])
def open_feedback_add():
    connection = []
    if session.get("admin"):
        id_to_add = request.args.get("id")
        try:
            connection = psycopg2.connect(
                host=host, user=user, password=password, database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, users.name, estimation, comment, to_char(created_date, 'dd-mm-yyyy'), users.user_id, 
                                    users.photo_way 
                                    FROM feedback_to_moderate
                                    INNER JOIN users ON feedback_to_moderate.user_id = users.user_id
                                    ORDER BY id ASC ;"""
                )
                feedback_to_add = ""
                rev_info = cursor.fetchall()

                # Получили все отзывы на модерацию,
                # чтобы получить нужный по ID и его в модерации удалить, а в основу добавить

                for i in rev_info:
                    if int(i[0]) == int(id_to_add):
                        feedback_to_add = i

                cursor.execute(
                    f"""Insert into feedback(user_id, estimation, comment, created_date, photo_way)
                     values({feedback_to_add[5]}, {feedback_to_add[2]},
                    '{feedback_to_add[3]}', '{feedback_to_add[4]}', '{feedback_to_add[6]}')"""
                )

                cursor.execute(
                    f"""Delete from feedback_to_moderate where id = {id_to_add}"""
                )

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        return redirect("/reviews_admin")
    else:
        return redirect("/")


@app.route("/delete_feedback/", methods=["GET"])
def open_feedback_delete():
    connection = []
    if session.get("admin"):
        id_to_delete = request.args.get("id")
        try:
            connection = psycopg2.connect(
                host=host, user=user, password=password, database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""Delete from feedback_to_moderate where id = {id_to_delete}"""
                )

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)

        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        return redirect("/reviews_admin")
    else:
        return redirect("/")


@app.route("/delete_answer/", methods=["GET"])
def open_answer_delete():
    connection = []
    if session.get("admin"):
        id_to_delete = request.args.get("id")
        try:
            connection = psycopg2.connect(
                host=host, user=user, password=password, database=db_name
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(f"""Delete from answers where id = {id_to_delete}""")

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)

        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        return redirect("/answers_admin")
    else:
        return redirect("/")


@app.route("/email_confirm")
def email_confirm():
    email = app.config["Email_confirm"][1]
    email_code = app.config["Email_confirm"][0]

    sender = "amirhusnutdinov800900@gmail.com"
    password_email = "smta gzvy aonh dccg"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    email_code = str(email_code)

    template = """<!DOCTYPE html>
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
                                                                                                                                            <amp-img alt="Alternate image text" src="./static/assets/images/logo.jpeg" style="border:0 solid #1e293b;border-radius:0;display:block;outline:0;text-decoration:none;width:100%;font-size:13px" width="1000" height="800" layout="responsive"></amp-img>
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
                                                                                                                        <p style="text-align:center">Ваш код поддтверждения</p>
                                                                                                                    </div>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr>
                                                                                                                <td align="left" style="font-size:0;padding:10px 25px;padding-top:0;padding-right:0;padding-bottom:24px;padding-left:0;word-break:break-word">
                                                                                                                    <div style="font-family:Helvetica;font-size:16px;font-weight:400;letter-spacing:0;line-height:1.5;text-align:left;color:#475569">
                                                                                                                        <p style="text-align:justify">&#xA0;</p>
                                                                                                                        <p style="text-align:justify">
                                                                                                                        <p style="text-align:justify">
                                                                                                                        <div class="statistics">
                                                                                                                <div style="width: 100%; max-width: 1230px; padding: 0 15px; margin: 0 auto;">
                                                                                                                    <div style="display: flex; flex-wrap: wrap;">
                                                                                                                        <div style="display: inline-block; vertical-align: top; margin-right: 10px;">
                                                                                                                            <div style=" margin-bottom: 10px; font-size: 70px; font-weight: 700; line-height: 1; margin-left: 120px;">"""+ email_code[0] +"""</div>
                                                                                                                           
                                                                                                                        </div>
                                                                                                                        <div style="display: inline-block; vertical-align: top; margin-right: 10px;">
                                                                                                                            <div style=" margin-bottom: 10px; font-size: 70px; font-weight: 700; line-height: 1;">"""+ email_code[1] +"""</div>
                                                                                                                       
                                                                                                                        </div>
                                                                                                                        <div style="display: inline-block; vertical-align: top; margin-right: 10px;">
                                                                                                                            <div style=" margin-bottom: 10px; font-size: 70px; font-weight: 700; line-height: 1;">"""+ email_code[2] +"""</div></div>
<div style="display: inline-block; vertical-align: top; margin-right: 10px;">
<div style=" margin-bottom: 10px; font-size: 70px; font-weight: 700; line-height: 1;">"""+ email_code[3] +"""</div>
                                                                                                                        </div>
                                                                                                                        <div style="display: inline-block; vertical-align: top; margin-right: 10px;">
                                                                                                                            <div style=" margin-bottom: 10px; font-size: 70px; font-weight: 700; line-height: 1;">"""+ email_code[4] +"""</div>
                                                                                                                          
                                                                                                                        </div>
                                                                                                                    </div>
                                                                                                        
                                                                                                                </div>    
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
                                                                                                                                <a href=" """+ general +""" " style="display:inline-block;background:#1e293b;color:#fff;font-family:Helvetica;font-size:16px;font-weight:400;line-height:1;letter-spacing:1px;margin:0;text-decoration:none;text-transform:none;padding:12px 24px 12px 24px;border-radius:4px" target="_blank" data-block-id="block2eve656" data-block-type="block" data-url-id="dacc0710-55a8-5092-ab24-11a0937fe0d4">Узнать Больше</a>
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
                </html> """

    try:
        server.login(sender, password_email)
        msg = MIMEText(template, "html")
        msg["From"] = sender
        msg["To"] = email
        msg["Subject"] = "Твой код подтверждения"
        server.sendmail(sender, email, msg.as_string())

        print("The message was sent successfully!")
        return redirect("/email_confirm_page")
    except Exception as _ex:
        print(f"{_ex}\nCheck your login or password please!")
        return redirect("/")


@app.route("/email_confirm_page", methods=["GET", "POST"])
def email_confirm_page():
    info = Account.email_confirm_page()
    if request.method == "GET":
        return info
    elif request.method == "POST":
        return redirect(info)
    else:
        return redirect("/")


@app.route("/reset_password")
def reset_password():
    info = Account.email_confirm_page()
    if request.method == "GET":
        return info
    elif request.method == "POST":
        return redirect(info)
    else:
        return redirect("/")


@app.route("/generate_post", methods=['GET', 'POST'])
def open_generate_post():
    if session.get("admin"):
        form = GeneratePageForm()
        connection = []
        try:
            connection = psycopg2.connect(
                host=host, user=user, password=password, database=db_name
            )
            connection.autocommit = True
            if request.method == 'GET':
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT text FROM gpt_info; """)
                    gpt_info = cursor.fetchall()[0][0]
                    return render_template("generate_post.html",
                                           **params_admin,
                                           gp_is="active",
                                           form=form,
                                           text=gpt_info,
                                           title="Генерация постов",
                                           )

            if request.method == 'POST':
                import g4f
                answer_for_gpt = form.request.data
                gpt_response = g4f.ChatCompletion.create(model=g4f.models.gpt_4,
                                                         messages=[{'role': 'user', 'content': f'{answer_for_gpt}'}])
                with connection.cursor() as cursor:
                    cursor.execute(f"""UPDATE gpt_info SET text='{gpt_response}';""")
                return redirect('/generate_post')
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
    else:
        return redirect("/")


@app.errorhandler(404)
def page_not_found(_):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_internal_server_error(_):
    return render_template("500.html"), 500


@app.errorhandler(400)
def page_bad_request(_):
    return render_template("400.html"), 400


@app.route("/pp/")
def open_pp():
    return render_template(
        "privacy_policy.html",
        title="Политика конфиденциальности персональных данных",
        login=session.get("authorization"),
        **params,
    )


app.register_blueprint(event_api.blueprint)

port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)
