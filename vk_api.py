import vk
import base64
import json
import time


class Api:
    def __init__(self, login, token_file='base', version='5.78', scope='offline', language='ru', apps=None):
        if apps is None:
            apps = [4580399, 6063639, 6063581, 6063579, 5821493, 6477148, 6477149, 6477150, 5286056]
        self.version = version
        if 'offline' in scope.split(','):
            self.scope = scope
        else:
            self.scope = scope + ',offline'
        self.login = login
        self.token_file_name = token_file
        self.apps = apps
        self.language = language
        self.accs = []
        self.session = None
        self.password = None
        self.counter = 0
        self.last_time = 0

    def call(self):
        if self.counter != len(self.accs) - 1:
            self.counter += 1
        else:
            self.counter = 1
        if time.time() - self.last_time >= 1 / 3 / len(self.accs):
            self.last_time = time.time()
        else:
            time.sleep(1 / 3 / len(self.accs) - (time.time() - self.last_time))
            self.last_time = time.time()
        return self.accs[self.counter - 1]

    def auth(self):
        def _auth_(self):
            self.password = input('pass from %s: ' % self.login)  # password from vk.com
            for every in self.apps:
                self.session = vk.AuthSession(app_id=every, user_login=self.login, user_password=self.password,
                                              scope=self.scope)
                self.accs.append(vk.API(self.session, lang=self.language, v=self.version))

        try:
            file = open(self.token_file_name, 'rb')
        except FileNotFoundError:
            _auth_(self)
            with open(self.token_file_name, 'wb') as file:
                _arr = {base64.b64encode(bytes(self.login,'utf-8')).decode('utf-8'): base64.b64encode(bytes(self.session.access_token,'utf-8')).decode('utf-8')}
                file.write(base64.b64encode(bytes(json.dumps(_arr),'utf-8')))
                del self.session
        else:
            data = json.loads(base64.b64decode(file.read()).decode('utf-8'))
            file.close()
            if base64.b64encode(bytes(self.login,'utf-8')).decode('utf-8') in data:
                token = base64.b64decode(bytes(data[base64.b64encode(bytes(self.login,'utf-8')).decode('utf-8')],'utf-8')).decode('utf-8')
                for every in self.apps:
                    self.accs.append(vk.API(
                        vk.AuthSession(app_id=every, access_token=token, scope=self.scope), lang=self.language,
                        v=self.version))
            else:
                _auth_(self)
                with open(self.token_file_name, 'wb') as file:
                    data[base64.b64encode(bytes(self.login,'utf-8')).decode('utf-8')] = base64.b64encode(self.session.access_token).decode('utf-8')
                    file.write(base64.b64encode(json.dumps(data)))
                    del self.session
