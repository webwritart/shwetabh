import os

from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from extensions import current_year
from operations.messenger import send_email


main = Blueprint('main', __name__, static_folder='static', template_folder='templates')


@main.route('/', methods=['GET', 'POST'])
def home():
    projects_dir = 'static/images/concepts/'
    project_list = os.listdir(projects_dir)
    return render_template('index.html',project_list=project_list, current_year=current_year)


@main.route('/concept_artworks', methods=['GET', 'POST'])
def concept_artworks():
    project = request.args.get('project')
    artworks_dir = 'static/images/concepts/' + project + '/'
    artwork_list = os.listdir(artworks_dir)
    artwork_url_list = []
    for artwork in artwork_list:
        if artwork != 'Hero.jpg':
            artwork_url = 'static/images/concepts/' + project + '/' + artwork
            artwork_url_list.append(artwork_url)
    return render_template('concept_artworks.html', project=project, artwork_url_list=artwork_url_list,
                           current_year=current_year)



@main.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        email2 = request.form.get('email2')
        msg = request.form.get('message')
        message = f'{msg}\n\n\nSENDER DETAILS:\nName: {name}\nEmail: {email}\n'

        success_msg = (f'Dear {name},\n\nThanks for sending me a message.\nI will get back to you as soon as possible.\nHave a nice day! '
                       f':)\n\n\nShwetabh Suman\nConcept Artist & Illustrator\nNew Delhi, India')

        if email == email2:
            send_email('IMPORTANT!! - Main Portfolio', ['shwetabhartist@gmail.com'], email, message, '', '')
            send_email('MESSAGE SENT - Shwetabh Suman', [email], 'shwetabhartist@gmail.com', success_msg, '', '')
            flash('Message sent successfully!', 'success')
        else:
            flash("The email doesn't match!", "error")
            return redirect(request.url)
    return render_template('contact.html', current_year=current_year)
