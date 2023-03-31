from flask import render_template, request
from Links import about_us, blog, reviews, answers, event1, authorization, general, cabinet, logout, delete


class CabinetPage:
    @staticmethod
    def account_cabinet(method, email, name, surname):
        if method == 'GET':
            return render_template('cabinet.html',
                                   general=general,
                                   about_us=about_us,
                                   blog=blog,
                                   reviews=reviews,
                                   answers=answers,
                                   event1=event1,
                                   authorization=authorization,
                                   cabinet=cabinet,
                                   logout=logout,
                                   delete=delete,
                                   email=email, name=name, surname=surname)
        elif method == 'POST':
            return [request.form['inp_email'], request.form['inp_name'], request.form['inp_surname'],
                    request.form['pass_old'], request.form['pass_new'], request.form['inlineRadioOptions']]
