from flask import render_template
from Links import params
from flask import session


class StartPage:
    @staticmethod
    def main():
        start_params = params.copy()
        del start_params["general"]
        return render_template(
            "start_page.html",
            **start_params,
            is_nav="__nav",
            is_mobile="_mobile",
            is_genreal_page="body_general_page",
            title="Mindease",
            login=session.get("authorization")
        )
