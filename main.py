from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from dotenv import load_dotenv
from WebServer import *
from NfeVix import *
from Email import *
import os

# CONFIGS
load_dotenv()

# WEBDRIVER
driver = "{}/chromedriver".format(os.getcwd())

# API CLASS (CONFIG AND ROUTES)
class API(object):

    @staticmethod
    def run():

        # CONFIGURE WEB SERVER
        web = WebServer(login=API.login, jwt_expire=os.getenv('JWT_EXPIRE'))

        # ADD YOUR ROUTES HERE
        web.add({ "url": "/", "callback": API.api_public, "methods": ['GET'] })
        web.add({ "url": "/baixar", "callback": API.api_baixar, "methods": ['GET'] })

        # RUN APP
        web.run(port=os.getenv('PORT') or 8080, debug=(os.getenv('MODE') != 'production'))

    # LOGIN CALLBACK [REQUIRED]

    @staticmethod
    def login(username, password):

        return 1 if username == 'root' and password == '1234' else 0

    # ROUTES

    @staticmethod
    def api_public(req):

        try: return { "message": "Bem-Vindo ao RPA!" }
        except Exception as e: return { "error": str(e) }

    @staticmethod
    @jwt_required(optional=False)
    def api_baixar(req):

        try:

            # obtem dados do corpo do post da requisicao
            post = req.get_json(force=True)
            email = post['email']
            login = post['login']
            senha = post['senha']
            ins = post['ins']
            mes = post['mes']

            # entra no site da prefeitura, baixa NFs e sai
            nf = NfeVix(driver, login, senha, ins)
            arquivo = nf.baixar(mes)
            nf.fechar()

            nome = os.path.basename(arquivo)
            mail = Email(os.getenv('EMAIL_SMTP'), os.getenv('EMAIL_PORT'), True)
            mail.login(os.getenv('EMAIL_LOGIN'), os.getenv('EMAIL_SENHA'), False)
            mail.add_file(arquivo).send(os.getenv('EMAIL_ASSUNTO'), os.getenv('EMAIL_FROM'), email)

            return { "message": "Arquivo compactado {} enviado para e-mail {}".format(nome, email) }

        except Exception as e: return { "error": str(e) }

if __name__ == '__main__':

    api = API()
    api.run()