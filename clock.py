import os
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask
import deleting
from model import db
import model

sched = BlockingScheduler()

app = Flask(__name__)

model.create_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


@sched.scheduled_job('interval', minutes=int(os.environ['CLOCK_INTERVAL']))
def timed_job():
    deleting.delete()

if __name__ == "__main__":
    sched.start()
    app.run(debug=True)