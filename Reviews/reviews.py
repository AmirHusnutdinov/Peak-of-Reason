from flask import render_template
from Links import about_us, blog, reviews, answers, event1, authorization, general


class Reviews:
    @staticmethod
    def reviews():
        return render_template('reviews_page.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               event1=event1,
                               authorization=authorization
                               )
