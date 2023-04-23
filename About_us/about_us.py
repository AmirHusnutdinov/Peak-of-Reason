from flask import render_template
from Links import params


class About:
    @staticmethod
    def about():
        return render_template('about_us.html', **params,
                               ab_is_active='active', title='About us')
