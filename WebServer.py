from flask_jwt_extended import JWTManager, create_access_token
from flask import Flask, jsonify, request
from functools import partial
from waitress import serve
import random
import string

class WebServer:

    def __init__(self, login, jwt_expire, login_error_msg=None):

        self.users = []
        self.routes = []
        self.login = login

        self.app = Flask(__name__)

        self.jwt(jwt_expire or 300, login_error_msg or "Invalid login")

    # RUN
    def run(self, port=8080, debug=False):

        try:

            # ADD ALL API ROUTES
            for conf in self.routes:

                self.app.add_url_rule(conf['url'], conf['url'], partial(conf['callback'], request), methods=conf['methods'])

            # RUN WEB SERVER ON WSGI IF IN PRODUCTION
            self.app.run(host="0.0.0.0", port=int(port), debug=True) if debug else serve(self.app, host="0.0.0.0", port=int(port))

        except Exception as e:

            print('ERROR [run]: {}'.format(str(e)))

    # JWT CONFIGURE
    def jwt(self, expire, error_msg):

        try:

            # GENERATE SECRET KEY FOR JWT
            secret = ''.join(random.choice(string.ascii_letters) for i in range(10))

            # CONFIGURE PARAMETERS VALUES FOR ACCESS TOKEN SECURITY SYSTEM
            self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(expire)
            self.app.config['JWT_HEADER_NAME'] = 'X-Auth-Token'
            self.app.config['JWT_ERROR_MESSAGE_KEY'] = 'error'
            self.app.config['PROPAGATE_EXCEPTIONS'] = True
            self.app.config['JWT_SECRET_KEY'] = secret
            self.app.config['JWT_HEADER_TYPE'] = ''
            jwt = JWTManager(self.app)

            @self.app.route('/auth', methods=['POST'])
            # AUTHENTICATION ROUTE
            def auth():

                try:

                    # GET JSON FROM POST BODY
                    data = request.get_json(force=True)

                    # CALL LOGIN METHOD PASSING USER DATA
                    id = self.login(data['username'], data['password'])

                    # IF USER ID IS NOT VALID, SEND ERROR RESPONSE TO CLIENT
                    if int(id) < 1: return jsonify(error=str(error_msg)), 403

                    # IF USER WAS FOUND, CREATE TOKEN AND SEND TO CLIENT
                    token = create_access_token(identity=int(id))
                    return jsonify(token=token), 200

                except Exception as e: raise e

        except Exception as e:

            print('ERROR [jwt]: {}'.format(str(e)))

    def add(self, conf={}):

        try:

            self.routes.append(conf)

        except Exception as e:

            print('ERROR [add]: {}'.format(str(e)))