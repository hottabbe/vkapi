from vk_api import *

api = Api(input('login: '))  # login from vk.com
api.auth()

print(api.call().users.get())
