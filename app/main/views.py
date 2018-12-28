from datetime import datetime
from flask import render_template, url_for
from .forms import NameForm
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=name) #references "templates folder in app"