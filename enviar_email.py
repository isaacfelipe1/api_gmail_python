import os
import pickle
# Gmail API uteis
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# para codificar/decodificar mensagem na base64
from base64 import urlsafe_b64decode, urlsafe_b64encode

# Para Lidar com tipos de anexação MIME
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

#(Solicitando todo o acesso)
ESCOPO = ['https://mail.google.com/']
email = 'ifdsl.lic20@uea.edu.br'
def autenticar_gmail():
    creditos =None
    #O pickle armazerna o acesso do utilizador e a refresca os tokens, e 
    # é criado automaticamente quando o fluxo de autorização é concluido pela primeira vez
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creditos = pickle.load(token)
    # se não houver credenciais (válidas disponivel), deixe o usuario efetuar login.
    if not creditos or not creditos.valid:
        if creditos and creditos.expired and creditos.refresh_token:
            creditos.refresh(Request())
        else:
            fluxo = InstalledAppFlow.from_client_secrets_file('credenciais.json', ESCOPO)
            creditos = fluxo.run_local_server(port=0)
        # Guarda as credenciais para a próxima exercução
        with open("token.pickle", "wb") as token:
            pickle.dump(creditos, token)
    return build('gmail', 'v1', credentials=creditos)
# obtendo o serviço de API do GMAIL
servico = autenticar_gmail()

# adiciona o anexo com o nome de ficheiro dado á mensagem dada
def juntar_anexo(mensagem_email, nome_arquivo):
    tipo_conteudo, codificacao = guess_mime_type(nome_arquivo)
    if tipo_conteudo is None or codificacao is not None:
        tipo_conteudo = 'application/octet-stream'
    tipo_principal, sub_tipo = tipo_conteudo.split('/', 1)
    if tipo_principal == 'text':
        abrir_arq = open(nome_arquivo, 'rb')
        mensgem = MIMEText(abrir_arq.read().decode(), _subtype=sub_tipo)
        abrir_arq.close()
    elif tipo_principal == 'image':
        abrir_arq = open(nome_arquivo, 'rb')
        mensgem = MIMEImage(abrir_arq.read(), _subtype=sub_tipo)
        abrir_arq.close()
    elif tipo_principal == 'audio':
        abrir_arq = open(nome_arquivo, 'rb')
        mensgem = MIMEAudio(abrir_arq.read(), _subtype=sub_tipo)
        abrir_arq.close()
    else:
        abrir_arq = open(nome_arquivo, 'rb')
        mensgem = MIMEBase(tipo_principal, sub_tipo)
        mensgem.set_payload(abrir_arq.read())
        abrir_arq.close()
    nome_arquivo = os.path.basename(nome_arquivo)
    mensgem.add_header('Content-Disposition', 'attachment', nome_arquivo=nome_arquivo)
    mensagem_email.attach(mensgem)

def contruir_mensagem(destinatario, assunto,body, anexo=[]):
    if not anexo: # nenhum anexo fornecido
        mensagem_email = MIMEText(body, 'html')
        mensagem_email['to'] = destinatario
        mensagem_email['from'] = email
        mensagem_email['subject'] = assunto    
    else:
        mensagem_email = MIMEMultipart()
        mensagem_email['to'] = destinatario
        mensagem_email['from'] = email
        mensagem_email['subject'] = assunto
        mensagem_email.attach(MIMEText(body))
        for nome_arquivo in anexo:
            juntar_anexo(mensagem_email, nome_arquivo)
    return {'raw': urlsafe_b64encode(mensagem_email.as_bytes()).decode()}

def send_message(servico, destinatario, assunto, body, anexo=[]):
    return servico.users().messages().send(
      userId="me",
      body=contruir_mensagem(destinatario, assunto, body, anexo)
    ).execute()
def send(usuario, assunto,body):
    send_message(servico, usuario, assunto, body)
if __name__ == '__main__':
         send("alfredobarros@bemol.com.br", "DESAFIO TALENT LAB ITACOATIARA","Olá, meu nome  é Isaac Felipe e estou participando do PROCESSO SELETIVO DA BEMOL DIGITAL")
         send("juanoliveira@bemol.com.br", "DESAFIO TALENT LAB ITACOATIARA","Olá, meu nome  é Isaac Felipe e estou participando do PROCESSO SELETIVO DA BEMOL DIGITAL")
         send("emariellealmeida@bemol.com.br", "DESAFIO TALENT LAB ITACOATIARA","Olá, meu nome  é Isaac Felipe e estou participando do PROCESSO SELETIVO DA BEMOL DIGITAL")
         

     
   
   