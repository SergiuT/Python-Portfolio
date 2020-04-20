from flask import Flask, render_template, url_for, request, redirect
import smtplib
import os
import csv
from email.message import EmailMessage

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html(page_name):
    return render_template(page_name)


def send_email(data):
    email = EmailMessage()
    email['from'] = data["email"]
    email['subject'] = data["subject"]
    email['to'] = "sergiutont2@gmail.com"

    email.set_content(data['message'])

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('sergiutont2@gmail.com', f"{os.environ['PASSWORD']}")
        smtp.send_message(email)
        print('Email sent!')


def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        send_email(data)
        return redirect('/thankyou.html')
    else:
        return 'wrong'
