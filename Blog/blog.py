from flask import render_template
from Links import about_us, blog, reviews, answers, event1, authorization, general


class Blog:
    @staticmethod
    def blog():
        return render_template('blog_page.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               event1=event1,
                               authorization=authorization
                               )
