from flask import render_template, request
from Links import blog_Admin, event_Admin, answers_Admin, reviews_Admin, general, photo_add_Admin, params_admin
import os
from werkzeug.utils import secure_filename
from Events.data.teen_events import Teen_events
from Events.data.adult_events import Adult_events
from Events.data.all_events import All_events
from Events.data import db_session_event

from Reviews.data import db_session_rev
from Reviews.data.rev import Feedback

from Admin.data import db_session_admin
from Admin.data.admin_rev import Feedback_Admin

from Answers.data import db_session_answers
from Answers.data.answer_db import Answer_db

from Blog.data import db_session_blog
from Blog.data.Post import Post


class Admin:
    @staticmethod
    def admin(method):
        if method == 'GET':
            return render_template('admin_page.html',
                                   **params_admin, bl_is='active'
                                   )
        elif method == 'POST':
            db_session_blog.global_init("Blog/db/resources.db")
            db_sess = db_session_blog.create_session()
            all_posts = db_sess.query(Post)
            ids = []
            for id_ in all_posts:
                ids.append(id_.id)
            post = Post()
            post.photo_name = request.form['inp1']
            post.name = request.form['inp2']
            post.signature = request.form['inp3']
            post.link = f'http://127.0.0.1:8080/blog/?page={(ids[-1] + 1)}'
            post.post_text = request.form['inp4']
            post.created_date = request.form['inp5']

            db_sess = db_session_blog.create_session()
            db_sess.add(post)
            db_sess.commit()

            return '/blog_admin'

    @staticmethod
    def admin_answers(method):
        db_session_answers.global_init("Answers/db/asks.db")
        db_sess = db_session_answers.create_session()
        all_answers = db_sess.query(Answer_db)
        answers_info = []
        for answers in all_answers:
            answers_info.append([answers.id,
                                 answers.email,
                                 answers.name,
                                 answers.answer])
        len_ans = len(answers_info)
        if method == 'GET':
            return render_template('admin_answers_page.html',
                                   **params_admin,
                                   remained=len_ans, an_is='active'
                                   )
        elif method == 'POST':
            delete_id = list(map(int, ''.join(request.form['inp1']).split()))
            for id_ in delete_id:
                deleted_answer = db_sess.query(Answer_db).filter(Answer_db.id == id_).first()
                db_sess.delete(deleted_answer)
                db_sess.commit()

            return '/answers_admin'

    @staticmethod
    def admin_rev(method):
        db_session_admin.global_init("Admin/db/feedback_to_moderate.db")
        db_session_rev.global_init("Reviews/db/feedback.db")

        db_sess_admin = db_session_admin.create_session()
        db_sess_rev = db_session_rev.create_session()

        all_rev = db_sess_admin.query(Feedback_Admin)
        rev_info = []
        for rev in all_rev:
            rev_info.append([rev.id,
                             rev.name,
                             rev.estimation,
                             rev.comment,
                             rev.created_date,
                             rev.photo])
        len_rev = len(rev_info)
        if method == 'GET':
            return render_template('rev_admin_page.html',
                                   **params_admin,
                                   review=rev_info,
                                   remained=len_rev, re_is='active')
        elif method == 'POST':
            for id2 in (request.form['inp1']).split():
                for item in rev_info:
                    if int(item[0]) == int(id2):
                        for i in db_sess_admin.query(Feedback_Admin):
                            if int(i.id) == int(id2):
                                db_sess_admin.delete(i)
                                db_sess_admin.commit()

            for id1 in (request.form['inp2']).split():
                for item in rev_info:
                    if int(item[0]) == int(id1):
                        rev = Feedback()
                        rev.name = item[1]
                        rev.estimation = item[2]
                        rev.comment = item[3]
                        rev.created_date = item[4]
                        rev.photo = item[5]
                        db_sess_rev.add(rev)
                        db_sess_rev.commit()

                        for i in db_sess_admin.query(Feedback_Admin):
                            if int(i.id) == int(id1):
                                db_sess_admin.delete(i)
                                db_sess_admin.commit()

            return '/reviews_admin'

    @staticmethod
    def add_photo(method, app):
        if method == 'GET':
            return render_template('add_new_image.html',
                                   **params_admin, ph_is='active')

        elif method == 'POST':
            if 'file' not in request.files:
                return request.url
            file = request.files['file']
            if file.filename == '':
                return request.url
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return '/add_photo_admin'

    @staticmethod
    def event_admin(method):
        if method == 'GET':
            return render_template('admin_event.html',
                                   **params_admin, ev_is='active'
                                   )
        elif method == 'POST':
            db_session_event.global_init("Events/db/activities.db")
            db_sess = db_session_event.create_session()
            all_posts = db_sess.query(Post)
            ids = []

            for id_ in all_posts:
                ids.append(id_.id)

            all_event = All_events()
            all_event.photo_name = request.form['inp1']
            all_event.name = request.form['inp2']
            all_event.signature = request.form['inp3']
            all_event.link = f'http://127.0.0.1:8080/events/?page={(ids[-1] + 1)}'
            all_event.created_date = request.form['inp5']

            db_sess.add(all_event)
            db_sess.commit()

            if request.form['class'] == 'Копилка возможностей' or\
                    request.form['class'] == 'Тренинги для подростков' or\
                    request.form['class'] == 'Ораторское искусство':
                teev_event = Teen_events()
                teev_event.photo_name = request.form['inp1']
                teev_event.name = request.form['inp2']
                teev_event.signature = request.form['inp3']

                if request.form['class'] == 'Копилка возможностей':
                    teev_event.link = all_event.link = f'http://127.0.0.1:8080/event/types/?page={(ids[-1] + 1)}pb=1'

                elif request.form['class'] == 'Тренинги для подростков':
                    teev_event.link = all_event.link = f'http://127.0.0.1:8080/event/types/?page={(ids[-1] + 1)}tt=1'

                elif request.form['class'] == 'Ораторское искусство':
                    teev_event.link = all_event.link = f'http://127.0.0.1:8080/event/types/?page={(ids[-1] + 1)}orator=1'

                teev_event.created_date = request.form['inp5']

                if request.form['class'] == 'Копилка возможностей':
                    teev_event.a_piggy_bank_of_possibilities = True

                elif request.form['class'] == 'Тренинги для подростков':
                    teev_event.trainings_for_teenagers = True

                elif request.form['class'] == 'Ораторское искусство':
                    teev_event.oratory = True

                db_sess.add(teev_event)
                db_sess.commit()

                return '/event_admin'

            elif request.form['class'] == 'Тренинги для родителей' or\
                    request.form['class'] == 'Индивидуальные консультации' or\
                    request.form['class'] == 'Искусство общения':
                adult_event = Adult_events
                adult_event.photo_name = request.form['inp1']
                adult_event.name = request.form['inp2']
                adult_event.signature = request.form['inp3']

                if request.form['class'] == 'Тренинги для родителей':
                    adult_event.link = all_event.link = f'http://127.0.0.1:8080/event/types/?page={(ids[-1] + 1)}tp=1'

                elif request.form['class'] == 'Индивидуальные консультации':
                    adult_event.link = all_event.link = f'http://127.0.0.1:8080/event/types/?page={(ids[-1] + 1)}ic=1'

                elif request.form['class'] == 'Искусство общения':
                    adult_event.link = all_event.link = f'http://127.0.0.1:8080/event/types/?page={(ids[-1] + 1)}ac=1'

                adult_event.created_date = request.form['inp5']

                if request.form['class'] == 'Тренинги для родителей':
                    adult_event.trainings_for_parents = True

                elif request.form['class'] == 'Индивидуальные консультации':
                    adult_event.individual_consultations = True

                elif request.form['class'] == 'Искусство общения':
                    adult_event.the_art_of_communication = True

                db_sess.add(adult_event)
                db_sess.commit()

                return '/event_admin'


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
