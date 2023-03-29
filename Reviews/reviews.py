from flask import render_template, request
from Links import about_us, blog, reviews, answers, event1, authorization, general, cabinet
from datetime import datetime


class Reviews:

    @staticmethod
    def get_date(date):
        day_list = ['первое', 'второе', 'третье', 'четвёртое',
                    'пятое', 'шестое', 'седьмое', 'восьмое',
                    'девятое', 'десятое', 'одиннадцатое', 'двенадцатое',
                    'тринадцатое', 'четырнадцатое', 'пятнадцатое', 'шестнадцатое',
                    'семнадцатое', 'восемнадцатое', 'девятнадцатое', 'двадцатое',
                    'двадцать первое', 'двадцать второе', 'двадцать третье',
                    'двадацать четвёртое', 'двадцать пятое', 'двадцать шестое',
                    'двадцать седьмое', 'двадцать восьмое', 'двадцать девятое',
                    'тридцатое', 'тридцать первое']
        month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                      'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
        date_list = date.split('-')
        return (day_list[int(date_list[0]) - 1] + ' ' +
                month_list[int(date_list[1]) - 1] + ' ' +
                date_list[2] + ' года')

    @staticmethod
    def reviews(method, rand_list):
        if method == 'GET':
            return render_template('reviews_page.html',
                                   general=general,
                                   about_us=about_us,
                                   blog=blog,
                                   reviews=reviews,
                                   answers=answers,
                                   event1=event1,
                                   authorization=authorization,
                                   reviews_=rand_list,
                                   cabinet=cabinet)
        elif method == 'POST':
            date = Reviews.get_date(''.join(str(datetime.today().strftime('%d-%m-%Y'))))
            return [request.form['inp1'],
                    request.form['inp2'],
                    request.form['inp3'],
                    date]
