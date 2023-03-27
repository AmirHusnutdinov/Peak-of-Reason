from flask import render_template, request
from Links import about_us, blog, reviews, answers, event1, authorization, general, register


class Admin:
    @staticmethod
    def admin(method):
        if method == 'GET':
            return render_template('admin_page.html', general=general,
                                   about_us=about_us,
                                   blog=blog,
                                   reviews=reviews,
                                   answers=answers,
                                   event1=event1,
                                   authorization=authorization,
                                   register=register)
        elif method == 'POST':
            return [render_template('admin_page.html', general=general,
                                    about_us=about_us,
                                    blog=blog,
                                    reviews=reviews,
                                    answers=answers,
                                    event1=event1,
                                    authorization=authorization,
                                    register=register),
                    [request.form['photo_name'],
                     request.form['name'],
                     request.form['signature'],
                     request.form['link'],
                     request.form['created_date'],
                     ]]
