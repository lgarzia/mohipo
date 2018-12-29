from datetime import datetime
from flask import render_template, url_for, redirect, session, flash, current_app
from .forms import NameForm
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    print(dir(current_app))
    name = None
    form = NameForm()
    print(f"before form validate {form.data}")
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.data['name']:
            flash('Looks like you changed your name')
        session['name'] = form.data['name']
        print(f"after form validate {form.data} {session}")
        form.name.data = ''
        return redirect(url_for('main.index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name')) #references "templates folder in app"