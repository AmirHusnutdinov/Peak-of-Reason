from flask import render_template
from Links import params


class StartPage:
    @staticmethod
    def main():
        return render_template('start_page.html',
                               **params, is_nav='__nav', title='Mindease'
                               )
