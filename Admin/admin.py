from Admin.generate_textform import GeneratePageForm
from database_query import database_query
from flask import render_template
from Admin.blog_adminform import BlogAdminForm
from Admin.event_adminform import EventAdminForm
from Links import params_admin
import os
from settings import UPLOAD_FOLDER


class Admin:
    @staticmethod
    def blog_admin():
        form = BlogAdminForm()
        if form.validate_on_submit():
            ids = database_query("""SELECT id FROM blog;""")
            if not ids:
                ids = [[0]]
            date = database_query("""SELECT to_char(current_date, 'dd-mm-yyyy');""")
            date = str(date[0])[2:-3]
            database_query(f"""INSERT INTO blog (id, name, signature, post_text, link, created_date, photo_way) VALUES
                                ('{int(ids[-1][0]) + 1}', '{form.name.data}', '{form.signature.data}', '{form.text.data}',
                                '/blog/?page={int(ids[-1][0]) + 1}', '{date}'::date, '{form.list_of_photos.data.strip()}');""")
            return "/blog_admin"
        items = os.listdir("static/assets/images/blog")
        return render_template(
            "admin/admin_blog_page.html",
            **params_admin,
            bl_is="active",
            form=form,
            items=items,
            title="Блог Админ панель",
        )

    @staticmethod
    def admin_answers(method):
        answers_info = database_query(f"""SELECT id, users.email, users.name, answer FROM answers
                    INNER JOIN users ON answers.user_id = users.user_id;""")
        len_ans = len(answers_info)
        if method == "GET":
            return render_template(
                "admin/admin_answers_page.html",
                **params_admin,
                remained=len_ans,
                answers=answers_info,
                an_is="active",
                title="Вопросы Админ панель",
            )

    @staticmethod
    def admin_rev(method):
        rev_info = database_query(f"""SELECT id, users.name, estimation, comment, to_char(created_date, 'dd-mm-yyyy'), users.user_id, 
                    users.photo_way 
                    FROM feedback_to_moderate
                    INNER JOIN users ON feedback_to_moderate.user_id = users.user_id
                    ORDER BY id ASC ;""")
        len_rev = len(rev_info)
        if method == "GET":
            return render_template(
                "admin/rev_admin_page.html",
                **params_admin,
                review=rev_info,
                remained=len_rev,
                re_is="active",
                directory=UPLOAD_FOLDER,
                title="Отзывы Админ панель",
            )

    @staticmethod
    def event_admin():
        form = EventAdminForm()
        if form.validate_on_submit():
            ids = database_query("""SELECT id FROM events ORDER BY id DESC;""")
            if not ids:
                ids = [1]
            adult, teen, music, ic, taoc, oratory_teen, yourself, communicate = (
                False, False, False, False, False, False, False, False)
            if form.category.data in [
                "Харизматичный оратор",
                "Искусство быть собой",
                "Искусство общения",
            ]:
                teen = True
                if form.category.data == "Харизматичный оратор":
                    link = f"/event/types/?page={(ids[0][0] + 1)}&ot=1"
                    oratory_teen = True

                elif form.category.data == "Искусство быть собой":
                    link = f"/event/types/?page={(ids[0][0] + 1)}&ay=1"
                    yourself = True

                elif form.category.data == "Искусство общения":
                    link = f"/event/types/?page={(ids[0][0] + 1)}&ac=1"
                    communicate = True

            elif form.category.data in [
                "Музыкальная терапия",
                "Харизматичный оратор 18+",
            ]:
                adult = True
                if form.category.data == "Музыкальная терапия":
                    link = f"/event/types/?page={(ids[0][0] + 1)}&mt=1"
                    music = True

                elif form.category.data == "Харизматичный оратор 18+":
                    link = f"/event/types/?page={(ids[0][0] + 1)}&oa=1"
                    ic = True

            ids = database_query("""SELECT id FROM events;""")
            if not ids:
                ids = [[0]]
            need_id = max(list(map(int, str(ids)[2:-3].replace(',),', '').split(' ('))))
            database_query(f"""insert into events 
                    (id, name, signature, created_date, link, photo_way,
                     is_teen, is_oratory_teen, is_taoby, is_taoc, 
                     is_adult, is_poebtmt, is_oratory_adult,
                    time, post_text, count_of_people, price, id_of_people)
                     values ('{need_id + 1}', '{form.name.data}', '{form.signature.data}', '{form.date.data}', '{link}',
                      '{form.photo_name.data}', 
                      '{teen}'::bool, '{oratory_teen}'::bool, '{yourself}'::bool, '{communicate}'::bool,
                      '{adult}'::bool, '{music}'::bool, '{ic}'::bool,
                       '{str(form.time.data)}', '{form.post_text.data}', '{form.count_of_people.data}',
                        '{form.price.data}'::int, '{{}}')""")
            return "/event_admin"
        items = os.listdir("static/assets/images/event")
        return render_template(
            "admin/admin_event.html",
            **params_admin,
            ev_is="active",
            form=form,
            items=items,
            title="События Админ панель",)

    @staticmethod
    def add_feedback(id_to_add):
        feedback_to_add = ""
        rev_info = database_query(f"""SELECT id, users.name, estimation, comment, to_char(created_date, 'dd-mm-yyyy'), users.user_id, 
                                    users.photo_way 
                                    FROM feedback_to_moderate
                                    INNER JOIN users ON feedback_to_moderate.user_id = users.user_id
                                    ORDER BY id ASC ;""")
        # Получили все отзывы на модерацию,
        # чтобы получить нужный по ID и его в модерации удалить, а в основу добавить
        for i in rev_info:
            if int(i[0]) == int(id_to_add):
                feedback_to_add = i
        database_query(f"""Insert into feedback(user_id, estimation, comment, created_date, photo_way)
             values({feedback_to_add[5]}, {feedback_to_add[2]},
            '{feedback_to_add[3]}', '{feedback_to_add[4]}', '{feedback_to_add[6]}')""")
        database_query( f"""Delete from feedback_to_moderate where id = {id_to_add}""")

    @staticmethod
    def generate_post(method):
        form = GeneratePageForm()
        if method == 'POST':
            import g4f
            answer_for_gpt = form.request.data
            gpt_response = g4f.ChatCompletion.create(model=g4f.models.gpt_4,
                                                     messages=[{'role': 'user', 'content': f'{answer_for_gpt}'}])
            database_query(f"""UPDATE gpt_info SET text='{gpt_response}';""")
        gpt_info = database_query("""SELECT text FROM gpt_info; """)[0][0]
        return render_template("admin/generate_post.html",
                               **params_admin,
                               gp_is="active",
                               form=form,
                               text=gpt_info,
                               title="Генерация постов", )


ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
