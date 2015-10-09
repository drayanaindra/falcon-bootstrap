from mongoengine import connect

connect(
    'col_apps',
    host='127.0.0.1',
    port=27017
    )
