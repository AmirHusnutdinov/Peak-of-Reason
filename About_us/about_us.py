from flask import render_template
from Links import about_us, blog, reviews, answers, events, authorization, general, cabinet


class About:
    @staticmethod
    def about():
        return render_template('about_us.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               events=events,
                               authorization=authorization,
                                   cabinet=cabinet
                               )
