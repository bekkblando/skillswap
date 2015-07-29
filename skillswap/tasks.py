from celery import Celery

app = Celery('tasks', backend='amqp', broker='amqp://guest:guest@localhost:5672/')



@app.task
def print_hello():
    print('hello there')