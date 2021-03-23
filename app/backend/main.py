import requests
import json
import os
# Importacao para geracao das senhas
import random
import string
# Importacao para envio do e-mail (SendGrid)
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# Importando flask
from flask import escape
from flask_cors import CORS, cross_origin

@cross_origin()
def recebe_requisicao(request):
    request_form = request.form

    if request_form and 'inputNome' and 'inputSobrenome' and 'inputEmail' in request_form:
        nome = request_form['inputNome']
        sobrenome = request_form['inputSobrenome']
        email = request_form['inputEmail']

        resultado = cria_usuario_moodle(email,nome,sobrenome)

        if resultado == 'sucesso':
            return 'Solicitação recebida com sucesso.'
        else:
            print('RR:ERRO:CRIACAO_DE_USUARIO_FALHOU')
            return 'Erro, entre em contato com o administrator do sistema.'
    else:
        print('RR:ERRO:PARAMETRO_NAO_ENCONTRADO')
        return 'Erro, entre em contato com o administrator do sistema.'

# Função criada para
# Gerar a senha aleatoria
def gerar_senha(numeroCaracteres):
    
    # Seleciona os tipos de caracteres utilizados
    #
    # string.ascii_letters = Letras a-z e A-Z
    # string.digits = Números de 0 a 9
    # string.punctuation = Caracteres especiais
    senha_caracteres = string.ascii_letters + string.digits # + string.punctuation

    # Dentro de um loop de "numeroCaracteres" pega caracater por caracter 
    # e concatena na variavel senha
    senha = ''.join(random.choice(senha_caracteres) for i in range(numeroCaracteres))

    # Retorna a senha
    return senha

# Função criada para
# Enviar e-mails
def enviar_email(dest_mail, dest_nome, assunto, mensagem):
    # E-mail do remetente
    email_remetente = os.environ.get('EMAIL_REMETENTE')
    
    # Cria mensagem para o destinatário
    message = Mail(
        from_email=email_remetente,
        to_emails=dest_mail,
        subject=assunto,
        html_content=mensagem
    )

    # Envia o e-mail
    try:
        print('Enviando e-mail para ' + dest_mail + ' com assunto ' + assunto)
        
        # Token da conta do SendGrid
        print('TOKEN = ' + os.environ.get('SENDGRID_TOKEN') )
        sg = SendGridAPIClient(os.environ.get('SENDGRID_TOKEN'))
        response = sg.send(message)
        print(response.status_code)
        print('E-mail enviado com sucesso!')
    except Exception as e:
        print(e)		

# Envia e-mail de novos cadastros
def enviar_email_novo_cadastro(dest_mail, dest_nome, usuario, senha_acesso, site):
    assunto = "[Treinamento] Novo Cadastro"
    mensagem = "<html><br>Bem vindo " + dest_nome + "!"
    mensagem+= "<br><br><b>Acesso ao sistema:</b>"
    mensagem+= "<br>- Endereço: http://" + site + "/my/"
    mensagem+= "<br>- Usuário: " + usuario
    mensagem+= "<br>- Senha: " + senha_acesso
    mensagem+= "<br><br>Atencionsamente,"
    mensagem+= "<br>Portal Treinamento Corporativo</html>"
    enviar_email(dest_mail, dest_nome,assunto,mensagem)


def cria_usuario_moodle(email,nome,sobrenome):
    
    token = os.environ.get('MOODLE_TOKEN')
    servidor = os.environ.get('MOODLE_SERVER')

    function = 'core_user_create_users'
    url = 'http://{0}/webservice/rest/server.php?wstoken={1}&wsfunction={2}&moodlewsrestformat=json'.format(servidor,token,function)

    print(cria_usuario_moodle)

    email = email
    username = email.split("@")[0]
    nova_senha = 'P#1' + gerar_senha(5)

    users = {'users[0][username]': username,
            'users[0][email]': email,
            'users[0][lastname]': sobrenome,
            'users[0][firstname]': nome,
            'users[0][password]': nova_senha} # Removida a senha padrão e colocado a função

    try:
        response = requests.post(url,data=users)
        if 'exception' in json.loads(response.text):
            print('Result: ' + response.text)
            return 'erro'
        else:
            print('Result: ' + response.text)
            # Cadastro com suceso enviar e-mail
            enviar_email_novo_cadastro(email, nome, username, nova_senha, servidor)
            return 'sucesso'
    except Exception as e:
        print(e)
        return 'erro'

