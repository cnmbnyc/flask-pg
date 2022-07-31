from flask import Flask
from celery import Celery

app = Flask(__name__)
app.config.update(
    CELERY_CONFIG={
        "broker_url": "redis://localhost:6379",
        "result_backend": "redis://localhost:6379",
    }
)


def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task()
def add_together(a, b):
    return a + b


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
