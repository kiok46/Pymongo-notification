# Pymongo-notification
Notifications from PyMongo to subscribers.

![ScreenShot](https://raw.github.com/kiok46/Pymongo-notification/master/screenshots/screenshot.png)
![ScreenShot](https://raw.github.com/kiok46/Pymongo-notification/master/screenshots/screenshot2.png)

### How to run?

To run the application at local you need to run these commands and should have python 3.6.1 in the system or in virtual environment.

Open terminal 1, cd to the folder and type the following commands to start virtual environment and celery worker.
```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
export MAIL_USERNAME="your_email_id"
export MAIL_PASSWORD="password"
celery worker -A app.celery --loglevel=debug
```

Open Terminal 2, cd to the folder and type the following command for running Redis server.
```
sudo chmod 755 run-redis.sh (if you don't have permission to run the script.)
./run-redis.sh
```

Open Terminal 3, cd to the folder and type the following commands to run the application
```
python3 app.py
```

and open the browser and paste http://127.0.0.1:5000/ in the address bar.

### MLab

Thanks to [MLab](https://mlab.com/) which provides 500MB free data upon signup which is perfect for such small experimental projects.

### TODO

 - Unsubscribe from the mails.
 - Run the method to send the mails in a task scheduler like celery.
 - Email validation.

### LICENSE

MIT License [LICENSE](https://github.com/kiok46/Pymongo-notification/blob/master/LICENSE)
