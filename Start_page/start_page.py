from flask import render_template
from Links import events, params


class StartPage:
    @staticmethod
    def main():
        return render_template('start_page.html',
                               **params, is_nav='__nav',
                               event1=events, title='Mindease'
                               )
