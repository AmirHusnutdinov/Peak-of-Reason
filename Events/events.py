from flask import render_template
from Links import about_us, blog, reviews, answers, event1, \
    event2, event3, event4, authorization, general, cabinet


class Events:
    @staticmethod
    def event1():
        return render_template('event1.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               event2=event2,
                               event3=event3,
                               event4=event4,
                               authorization=authorization,
                               cabinet=cabinet
                               )

    @staticmethod
    def event2():
        return render_template('event2.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               event1=event1,
                               event3=event3,
                               event4=event4,
                               authorization=authorization,
                               cabinet=cabinet
                               )

    @staticmethod
    def event3():
        return render_template('event3.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               event2=event2,
                               event1=event1,
                               event4=event4,
                               authorization=authorization,
                               cabinet=cabinet
                               )

    @staticmethod
    def event4():
        return render_template('event4.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               event2=event2,
                               event3=event3,
                               event1=event1,
                               authorization=authorization,
                               cabinet=cabinet
                               )
