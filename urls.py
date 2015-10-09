import falcon

from apps import *

app = falcon.API()

app.add_route('/members', app_member)
app.add_route('/members/create', app_member)
app.add_route('/members/{action}/{id}', app_member)