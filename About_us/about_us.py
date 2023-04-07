from flask import render_template
from Links import about_us, blog, reviews, answers, event1, authorization, general, cabinet


class About:
    @staticmethod
    def about():
        return render_template('about_us.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               event1=event1,
                               authorization=authorization,
                                   cabinet=cabinet
                               )
