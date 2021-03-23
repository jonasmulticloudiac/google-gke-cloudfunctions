# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
import requests
from flask import escape
from flask_cors import CORS, cross_origin
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email=os.environ.get('REMETENTE'),
    to_emails= maildest,
    subject='Envio de Emails - Gestão Talentos',
    html_content=msg
    )
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)

def send_emails(maildest, name , user, passwd, url):
    msg= "<br>- Dados de acesso ao portal: http://" + url 
    msg+= "<br>- Nome: " + user
    msg+= "<br>- Senha:"  + passwd
    enviar_email(maildest, name, msg)

### codigo do bootcamp 
def cria_usuario_moodle(email,nome,sobrenome):
    
    token = os.environ.get('MOODLE_TOKEN')
    servidor = os.environ.get('MOODLE_SERVER')

    function = 'core_user_create_users'
    url = 'http://{0}/webservice/rest/server.php?wstoken={1}&wsfunction={2}&moodlewsrestformat=json'.format(servidor,token,function)

    print(cria_usuario_moodle)

    email = email
    username = email.split("@")[0]
    passwd = 'criarHashAutomatica'

    users = {'users[0][username]': username,
            'users[0][email]': email,
            'users[0][lastname]': sobrenome,
            'users[0][firstname]': nome,
            'users[0][password]':  passwd} # precisa criar uma logica de senha randomica

    try:
        response = requests.post(url,data=users)
        if 'exception' in json.loads(response.text):
            print('Result: ' + response.text)
            return 'erro'
        else:
            print('Result: ' + response.text)
            send_emails(email, nome, username, passwd, servidor)
            return 'sucesso'
    except Exception as e:
        print(e)
        return 'erro'

