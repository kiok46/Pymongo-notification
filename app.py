"""
KULDEEP SINGH
"""

from flask import Flask, request, g, render_template, Response, jsonify
from flask import session, flash, redirect, url_for, make_response

from flask_pymongo import PyMongo
from flask_mail import Mail, Message
import config_ext
import os


app = Flask(__name__)

# --- MongoDB configs. --- #

app.config['MONGO_DBNAME'] = config_ext.mongo_dbname
app.config['MONGO_URI'] = config_ext.mongo_uri

mongo = PyMongo(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# Thanks to the unknown spammer who told me that I added my email password. :P
app.config['MAIL_DEFAULT_SENDER'] = 'testskuldeep@gmail.com'


mail = Mail(app)


@app.route('/')
def index():
    '''
    Entry point.
    '''
    message = ""
    return render_template("index.html", message=message)


@app.errorhandler(404)
def not_found(error):
    '''
    Handles if 404 occurs.
    '''
    return render_template("404.html")


def find_subscribed_users(db, *args):
    '''
    Method finds subscribed users and sends them a mail about the
    changes in the database.
    '''
    subscribers = db.find({"user_activated_subscription": False})
    recipients = []
    for s in subscribers:
        user_info = list(s.values())
        user_email = user_info[2]
        recipients.append(user_email)

    title = "Hi subscriber user"
    sender = 'testskuldeep@gmail.com'
    
    recipients.append("kuldeepbb.grewal@gmailcom")
    body = "There was some change in the database."

    msg = Message(title, sender=sender,
                  recipients=recipients, body=body)

    mail.send(msg)


@app.route('/subscribed', methods=['GET', 'POST'])
def subscribe():
    '''
    Subscription to the email notifications.
    '''
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']

        if request.form.getlist('activate_subscription'):
            user_activated_subscription = True
        else:
            user_activated_subscription = False

        db = mongo.db.MongoNotify
        db.create_index("user_email", unique=True)

        try:
            db.insert(
                {
                    "user_name": user_name,
                    "user_email": user_email,
                    "user_activated_subscription": user_activated_subscription
                })
            find_subscribed_users(db)
            return render_template("subscribed.html", user_name=user_name,
                                   user_email=user_email,
                                   user_activated_subscription=user_activated_subscription)
        except:
            message = "Email already taken."
            return render_template("index.html", message=message)

    return render_template("index.html")


@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    '''
    Unsubscribe from the notifications.
    '''

    return render_template("unsubscribe.html")


if __name__ == "__main__":
    app.run()
