from flask import render_template
from Links import about_us, blog, reviews, answers, events, authorization, general


class Reviews:
    @staticmethod
    def reviews():
        return render_template('reviews_page.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               events=events,
                               authorization=authorization
                               )
