from flask import render_template


class StartPage:

    def main(self):
        return render_template('start_page.html')
