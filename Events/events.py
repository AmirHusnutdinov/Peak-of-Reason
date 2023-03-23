from flask import render_template
from Links import about_us, blog, reviews, answers, events, authorization, general


class Events:
    @staticmethod
    def event():
        return render_template('event1.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               events=events,
                               authorization=authorization
                               )
