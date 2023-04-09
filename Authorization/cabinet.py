from flask import render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash

from Authorization.account import password_check
from Authorization.data import db_session_accaunt
from Authorization.data.users import Users
from Links import about_us, blog, reviews, answers, event1, authorization, general, cabinet, logout, delete


class CabinetPage:
    @staticmethod
    def account_cabinet(method):
        db_sess_cabinet = db_session_accaunt.create_session()
        all_information_cabinet = db_sess_cabinet.query(Users)
        if method == 'GET':
            for i in all_information_cabinet:
                if i.id == session.get('id'):
                    email = i.email
                    name = i.name
                    surname = i.surname
                    gender = i.gender
                    break
            if gender == 'male':
                male = 'checked'
                female = ''
            else:
                male = ''
                female = 'checked'
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
                                   email=email, name=name, surname=surname,
                                   male=male, female=female)
        elif method == 'POST':
            mass_cabinet = [request.form['inp_email'], request.form['inp_name'], request.form['inp_surname'],
                            request.form['pass_old'], request.form['pass_new'], request.form['inlineRadioOptions']]

            users = db_sess_cabinet.query(Users).filter(Users.id == session.get('id')).first()
            if not check_password_hash(users.password, mass_cabinet[3]) and mass_cabinet[3] != '':
                flash('Это не ваш старый пароль')
                return '/cabinet'
            if users.email != mass_cabinet[0] and mass_cabinet[0] != '':
                if db_sess_cabinet.query(Users).filter(Users.email == mass_cabinet[0]).first():
                    flash("Такой пользователь с такой почтой уже зарегистрирован")
                    return '/cabinet'
                else:
                    users.email = mass_cabinet[0]
            if users.name != mass_cabinet[1] and mass_cabinet[1].strip() != '':
                if mass_cabinet[1].strip() == '':
                    flash("Укажите имя")
                    return '/cabinet'
                elif len(mass_cabinet[1].strip()) <= 1:
                    flash("Имя не может состоять из одного символа")
                    return '/cabinet'
                else:
                    users.name = mass_cabinet[1]
            if users.surname != mass_cabinet[2] and mass_cabinet[2].strip() != '':
                if mass_cabinet[2].strip() == '':
                    flash("Укажите фамилию")
                    return '/cabinet'
                elif len(mass_cabinet[2].strip()) <= 1:
                    flash("Фамилия не может состоять из одного символа")
                    return '/cabinet'
                else:
                    users.surname = mass_cabinet[2]
            if mass_cabinet[4].strip() != '' and mass_cabinet[3].strip() != '':
                if password_check(mass_cabinet[4]) != mass_cabinet[4]:
                    flash(password_check(mass_cabinet[4]))
                    return '/cabinet'
                else:
                    users.password = generate_password_hash(mass_cabinet[4])
            if users.gender != mass_cabinet[5]:
                users.gender = mass_cabinet[5]
            db_sess_cabinet.merge(users)
            db_sess_cabinet.commit()

        return '/cabinet'
