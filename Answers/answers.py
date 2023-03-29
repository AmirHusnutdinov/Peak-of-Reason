from flask import render_template, request
from Links import about_us, blog, reviews, answers, event1, authorization, general, register, cabinet


class Answers:
    @staticmethod
    def answers(method):
        if method == 'GET':
            return render_template('answers_page.html',
                                   general=general,
                                   about_us=about_us,
                                   blog=blog,
                                   reviews=reviews,
                                   answers=answers,
                                   event1=event1,
                                   authorization=authorization,
                                   cabinet=cabinet
                                   )
        elif method == 'POST':
            return [request.form['inp1'], request.form['inp2'], request.form['inp3']]
