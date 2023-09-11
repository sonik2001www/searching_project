from celery import Celery

app = Celery('proj',
             broker='pyamqp://guest@localhost//',  # Адреса брокера
             backend='rpc://',
             include=['parser_app.tasks'])

# Опціональна конфігурація, дивіться у документації Celery.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
