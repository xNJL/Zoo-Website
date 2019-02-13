from flask import render_template, redirect, url_for
from flask_login import current_user

from . import bp


@bp.route('/')
def home_page():
    if current_user.is_authenticated:
        if current_user.user_type == "ADMIN":
            return redirect(url_for('admin.admin'))

        elif current_user.user_type == "STAFF":
            return redirect(url_for('staff.staff'))

        elif current_user.user_type == "VISITOR":
            return redirect(url_for('visitor.visitor'))

    return render_template('main/home_page.html', title='Home')
