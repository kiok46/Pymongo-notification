"""
KULDEEP SINGH
"""

from flask import Flask, request, g, render_template, Response, jsonify
from flask import session, flash, redirect, url_for, make_response

from flask_pymongo import PyMongo

import config_ext


app = Flask(__name__)
# --- MongoDB configs. --- #
# Configure the app, these congifuration were given at the time of creation an account
# on mlab.com .5GB free.
app.config['MONGO_DBNAME'] = config_ext.mongo_dbname
app.config['MONGO_URI'] = config_ext.mongo_uri

mongo = PyMongo(app)





@app.route('/')
def index():
    '''
    Entry point.
    '''
    return render_template("index.html")


@app.errorhandler(404)
def not_found(error):
    '''
    Handles if 404 occurs.
    '''
    return render_template("404.html")


@app.route('/subscribed', methods=['GET', 'POST'])
def subscribe():
    '''
    Subscription.
    '''
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        if request.form.getlist('activate_subscription'):
            user_activated_subscription = True
        else:
            user_activated_subscription = False

        db = mongo.db.MongoNotify
        try:
            db.insert(
                {
                    "user_name": user_name,
                    "user_email": user_email,
                    "user_activated_subscription": user_activated_subscription
                })
        except:
            raise Exception("Unable to add.") 

        return render_template("subscribed.html", user_name=user_name,
                               user_email=user_email,
                               user_activated_subscription=user_activated_subscription)

    return render_template("index.html")


@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    '''
    Unsubscribe.
    '''

    return render_template("unsubscribe.html")


if __name__ == "__main__":
    app.run(debug=True)
