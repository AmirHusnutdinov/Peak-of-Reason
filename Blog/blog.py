from flask import render_template
from Links import about_us, blog, reviews, answers, events, authorization, general
from data import db_session


class Blog:
    @staticmethod
    def blog():
        db_session.global_init("db/blogs.db")
        return render_template('blog_page.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               events=events,
                               authorization=authorization
                               )
