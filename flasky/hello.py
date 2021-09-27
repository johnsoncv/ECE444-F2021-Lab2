from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Email, ValidationError
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Trident'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('What is your UofT email address?', validators=[Required(), Email()])
    submit = SubmitField('Submit')

    def validate_email(form,  field):
        if "utoronto" not in field.data:
            raise ValidationError("Please use your UofT email")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
    
if __name__ == '__main__':    
    app.run(debug=True)
