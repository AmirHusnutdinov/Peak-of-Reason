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
    info = Reviews.reviews(request.method)
    if request.method == "GET":
        return info
    elif request.method == "POST":
        return redirect(info)


@app.route("/events/")
def open_events():
    return Events.events()


@app.route("/event/")
def open_event1():
    query1 = request.args.get("teen")
    query2 = request.args.get("adult")
    query3 = request.args.get("mt")
    query4 = request.args.get("oa")
    query5 = request.args.get("ac")
    query6 = request.args.get("ay")
    query7 = request.args.get("ot")
    return Events.filtering_events(query1, query2, query3, query4, query5, query6, query7)


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
            req = Events.event_buy_pages(int(page))
            if req:
                return req
            else:
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
            req = Events.event_confirm(event, user_id)
            if req:
                return redirect(f"/event/buy/?page={int(event)}")
            else:
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
        info = Admin.blog_admin()
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
            "admin/add_new_image.html",
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
                "admin/add_new_image.html",
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
    if session.get("admin"):
        id_to_add = request.args.get("id")
        Admin.add_feedback(id_to_add)
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
    template = '\n'.join(open('email.txt').readlines())
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
        return Admin.generate_post(request.method)
    else:
        return redirect("/")


@app.errorhandler(404)
def page_not_found(_):
    return render_template("error_codes/404.html"), 404


@app.errorhandler(500)
def page_internal_server_error(_):
    return render_template("error_codes/500.html"), 500


@app.errorhandler(400)
def page_bad_request(_):
    return render_template("error_codes/400.html"), 400


@app.route("/pp/")
def open_pp():
    return render_template(
        "cabinet/privacy_policy.html",
        title="Политика конфиденциальности персональных данных",
        login=session.get("authorization"),
        **params,
    )


app.register_blueprint(event_api.blueprint)

port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)
