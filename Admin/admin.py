from flask import render_template, request
from Links import about_us, blog, reviews, answers, event1, authorization, general


class Admin:
    @staticmethod
    def admin(method):
        if method == 'GET':
            return render_template('admin_page.html',
                                   general=general,
                                   about_us=about_us,
                                   blog=blog,
                                   reviews=reviews,
                                   answers=answers,
                                   event1=event1,
                                   authorization=authorization
                                   )
        elif method == 'POST':
            return [render_template('admin_page.html',
                                    general=general,
                                    about_us=about_us,
                                    blog=blog,
                                    reviews=reviews,
                                    answers=answers,
                                    event1=event1,
                                    authorization=authorization
                                    ), [request.form['inp1'], request.form['inp2'],
                                        request.form['inp3'], request.form['inp4'],
                                        request.form['inp5']]]
