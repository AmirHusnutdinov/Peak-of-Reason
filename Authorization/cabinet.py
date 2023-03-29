from flask import render_template
from Links import about_us, blog, reviews, answers, event1, authorization, general, cabinet


class CabinetPage:
    @staticmethod
    def account_cabinet():
        return render_template('cabinet.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               event1=event1,
                               authorization=authorization,
                               cabinet=cabinet)
