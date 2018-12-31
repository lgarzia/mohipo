from datetime import datetime
from flask import render_template, url_for, redirect, session, flash, current_app
from .forms import NameForm
from . import main
from ..models import User, Role
from .. import db
from ..email import send_email
from flask_login import login_required # Protect Routes

@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed'


@main.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm() #name/role
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.data['name']:
            flash('Looks like you changed your name')
        session['name'] = form.data['name']
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            role = Role(name=form.role.data)
            db.session.add(role)
            db.session.commit()
            role_id = role.id
            print(f"role_id is {role_id}")
            user = User(username=form.name.data, role_id=role_id)
            db.session.add(user)
            db.session.commit()
            send_email(to='lgarzia@yahoo.com', subject='Testing emails',
                       template='mail/new_user', name="LUKE")
            print(f"user_id is {user.id}")
        print(f"user is {user}")
        form.name.data = ''
        return redirect(url_for('main.index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name')) #references "templates folder in app"