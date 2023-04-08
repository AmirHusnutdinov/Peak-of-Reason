from flask import render_template
from Links import about_us, blog, reviews, answers, events, authorization, general, cabinet


class StartPage:
    @staticmethod
    def main():
        return render_template('start_page.html',
                               general=general,
                               about_us=about_us,
                               blog=blog,
                               reviews=reviews,
                               answers=answers,
                               events=events,
                               authorization=authorization,
                               cabinet=cabinet
                               )
