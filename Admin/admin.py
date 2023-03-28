from flask import render_template, request
from Links import blog_Admin, event_Admin, answers_Admin, reviews_Admin, general


class Admin:
    @staticmethod
    def admin(method):
        if method == 'GET':
            return render_template('admin_page.html',
                                   general=general,
                                   blog_Admin=blog_Admin,
                                   event_Admin=event_Admin,
                                   answers_Admin=answers_Admin,
                                   reviews_Admin=reviews_Admin
                                   )
        elif method == 'POST':
            return [render_template('admin_page.html',
                                    general=general,
                                    blog_Admin=blog_Admin,
                                    event_Admin=event_Admin,
                                    answers_Admin=answers_Admin,
                                    reviews_Admin=reviews_Admin
                                    ), [request.form['inp1']]]

    @staticmethod
    def admin_answers(method, answers):
        len_ans = len(answers)
        if method == 'GET':
            return render_template('admin_answers_page.html',
                                   general=general,
                                   blog_Admin=blog_Admin,
                                   event_Admin=event_Admin,
                                   answers_Admin=answers_Admin,
                                   reviews_Admin=reviews_Admin,
                                   answers=answers,
                                   remained=len_ans
                                   )
        elif method == 'POST':
            return [render_template('admin_answers_page.html',
                                    general=general,
                                    blog_Admin=blog_Admin,
                                    event_Admin=event_Admin,
                                    answers_Admin=answers_Admin,
                                    reviews_Admin=reviews_Admin,
                                    answers=answers
                                    ), [request.form['inp1']]]
