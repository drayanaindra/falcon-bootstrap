import falcon
import json

from documents.contact import Member, ProfileMember


class AppMember(object):
    """
    data when user register
    {
        "username": "user_name",
        "email": "username@email.com",
        "address": "address user",
        "name": "Member name"
    }

    data when user not register
    {
        "email": "username@email.com",
        "address": "address user",
        "name": "Member name"
    }
    """
    def on_post(self, req, resp, **kwargs):
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'error', ex.message)

        result_json = json.loads(raw_json, encoding='utf-8')

        if kwargs.get('action') == 'edit':
            id_data = kwargs.get('id')
            try:
                get_member = Member.objects.get(id=id_data)
                get_mempro = ProfileMember.objects.get(user=get_member.id)

                get_member.name = result_json.get('name')
                get_member.email = result_json.get('email')
                get_member.username = result_json.get('username')
                get_member.save()

                get_mempro.address = result_json.get('address')
                get_mempro.save()
            except Member.DoesNotExist:
                try:
                    get_mempro = ProfileMember.objects.get(id=id_data)
                    get_mempro.name = result_json.get('name')
                    get_mempro.email = result_json.get('email')
                    get_mempro.address = result_json.get('address')
                    get_mempro.save()
                except ProfileMember.DoesNotExist:
                    raise falcon.HTTPError(falcon.HTTP_400, "error", "data can't edited!")
            except:
                raise falcon.HTTPError(falcon.HTTP_400, "error", "data can't edited!")

            resp.status = falcon.HTTP_200
            resp.body = json.dumps({'message': 'update data success!'})
        else:
            if result_json.get('username'):
                try:
                    get_member = Member.objects.get(username=result_json.get('username'))
                    raise falcon.HTTPForbidden("error", "username {u} already exist!".format(u=get_member.username))
                except Member.DoesNotExist:
                    member = Member.objects.create(
                        username=result_json.get('username'),
                        email=result_json.get('email'),
                        name=result_json.get('name')
                    )

                    profile_member = ProfileMember()
                    profile_member.user = member
                    profile_member.address = result_json.get('address')
                    profile_member.save()

                    user = str(profile_member.user.name)
                else:
                    profile_member = ProfileMember()
                    profile_member.name = result_json.get('name')
                    profile_member.address = result_json.get('address')
                    profile_member.email = result_json.get('email')
                    profile_member.save()

                    user = str(profile_member.name)

                data = {
                    'status': 'success',
                    'message': "member {u} created!".format(u=user)
                }

                resp.status = falcon.HTTP_200
                resp.body = json.dumps(data)

    def on_get(self, req, resp, **kwargs):
        action = kwargs.get('action')
        id_data = kwargs.get('id')
        list_data = []

        if action == 'detail' and id_data:
            try:
                mempro_id = kwargs.get('id')
                get_mempro = ProfileMember.objects.get(id=mempro_id)
            except ProfileMember.DoesNotExist:
                get_mempro = ProfileMember.objects.get(user=id_data)

            if get_mempro.user:
                list_data = {
                    'id': str(get_mempro.user.id),
                    'name': get_mempro.user.name,
                    'email': get_mempro.user.email,
                    'username': get_mempro.user.username,
                    'address': get_mempro.address,
                    'register': True,
                    'created': str(get_mempro.created_on)
                }
            else:
                list_data = {
                    'id': str(get_mempro.id),
                    'name': get_mempro.name,
                    'email': get_mempro.email,
                    'address': get_mempro.address,
                    'created': str(get_mempro.created_on)
                }
        elif action == 'delete' and id_data:
            try:
                get_member = Member.objects.get(id=id_data)
                get_member.delete()

                list_data = {'message': 'deleted success!'}
            except Member.DoesNotExist:
                try:
                    get_mempro = ProfileMember.objects.get(id=id_data)
                    get_mempro.delete()

                    list_data = {'message': 'deleted success!'}
                except ProfileMember.DoesNotExist:
                    list_data = {'error': 'deleted not success!'}
        else:
            list_member = ProfileMember.objects.all()
            if list_member:
                for item in list_member:
                    if item.user:
                        data = {
                            'id': str(item.user.id),
                            'name': item.user.name,
                            'username': item.user.username,
                            'address': item.address,
                            'email': item.user.email,
                            'is_register': True,
                            'created': str(item.created_on)
                        }
                    else:
                        data = {
                            'id': str(item.id),
                            'name': item.name,
                            'email': item.email,
                            'address': item.address,
                            'created': str(item.created_on)
                        }
                    list_data.append(data)
            else:
                list_data = {
                    'message': 'Data not found'
                }

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(list_data)