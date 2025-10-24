from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from extensions import current_year
from operations.messenger import send_email


main = Blueprint('main', __name__, static_folder='static', template_folder='templates')


@main.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', current_year=current_year)


@main.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        email2 = request.form.get('email2')
        msg = request.form.get('message')
        message = f'{msg}\n\n\nSENDER DETAILS:\nName: {name}\nEmail: {email}\n'

        success_msg = (f'Dear {name},\n\nThanks for sending me a message.\nI will get back to you as soon as possible. '
                       f':)\n\n\nShwetabh Suman\nConcept Artist & Illustrator\nNew Delhi, India')

        if email == email2:
            send_email('IMPORTANT!! - Illustrations Portfolio', ['shwetabhartist@gmail.com'], email, message, '', '')
            send_email('MESSAGE SENT - Shwetabh Suman', [email], 'shwetabhartist@gmail.com', success_msg, '', '')
            flash('Message sent successfully!', 'success')
        else:
            flash("The email doesn't match!", "error")
            return redirect(request.url)
    return render_template('contact.html', current_year=current_year)
