import pathlib
import re
import smtplib
import datetime
import time
import ssl
from xml.etree.ElementTree import tostring
import cx_Oracle
#librerias html estructura
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

EMAIL_SERVER = "" #servidor de correo
EMAIL_PORT = 465  
EMAIL_USER = "" # Cuenta desde donde se envian los correos
EMAIL_PASSWORD = ""
MAX_EMAILS_PER_HOURS = 100
#lectura de html
path=str( pathlib.Path().absolute())
html=open(path+"\index.html",'r')
CONTENT_TO_SEND = html.read()
html.close()
# Asunto y contenido del mail
SUBJECT_TO_SEND = "¡Feliz cumpleaños!"
#CONTENT_TO_SEND = open(path+"\index.html",'r').read()
#Tomar el texto plano y convertirlo a html
html=MIMEText(CONTENT_TO_SEND,'html')



def email_validation(email_to_validate):
     # Esta funcion se encarga de evaluar si un email posee una estructura correcta
     # Y devuelve True si es un correo valido, y False caso contrario.
     if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', email_to_validate.lower()):
          print("[INFO] {} es valido.".format(email_to_validate))
          return True
     else:
          print("[INFO] {} no es valido.".format(email_to_validate))
          return False

def store_error(line):
     # Esta funcion se encarga de crear y almacenar en un archivo txt (como nombre
     # tendra log_error_ seguido de la fecha del dia) la línea de datos en donde se
     # ha producido un error: [RUNTIME_ERROR], [SMTP_SERVER_ERROR], [SMTP_SERVER_ERROR]
     name_file_error = str(datetime.datetime.now())[:10]
     file_error = open("log_error_birthday" + name_file_error + ".txt","a")
     file_error.write(line +'\n')
     file_error.close()

def store_mail_sent_successfully(line):
     # Esta funcion se encarga de crear y almacenar en un archivo txt (como nombre
     # tendra log_mail_sent_successfully_ seguido de la fecha del dia) la línea de datos
     # enviada exitosamente
     file_name = str(datetime.datetime.now())[:10]
     file_successfully = open("log_mail_sent_birthday" + file_name + ".txt","a")
     file_successfully.write(line +'\n')
     file_successfully.close()

def send_email(email_receiver, subject, content):
     #return True
     # Esta funcion se encarga de realizar ele envio del correo dado el email del receptor,
     # asunto y contenido.
     sended_mail = False
     # Parámetros del mensaje
     password = EMAIL_PASSWORD
     #Estructura del mensaje
     msg=MIMEMultipart('related')
     msg['Subject']=subject
     msg['From']=EMAIL_USER
     msg['To'] = email_receiver
     msg.preamble = 'Multi-part message in MIME format.'

     msgHtml=MIMEMultipart('alternative')
     msgHtml.attach(content)

     msg.attach(msgHtml)
     ##Lectura de imágenes
     
     """ fp=open(path+'\\images\\image-2.png','rb')
     msgHBD=MIMEImage(fp.read())
     fp.close()
     msgHBD.add_header('Content-ID','<image2>')
     msgHBD.add_header('Content-Disposition', 'inline', filename='HB')
     msg.attach(msgHBD) """

     """ fpl=open(path+'\\images\\logo.png','rb')
     msgLogo=MIMEImage(fpl.read())
     fpl.close()
     msgLogo.add_header('Content-ID','<logo>')
     msgLogo.add_header('Content-Disposition', 'inline', filename='logo')
     msg.attach(msgLogo) """


     context = ssl.create_default_context()

     try:
          server = smtplib.SMTP_SSL(EMAIL_SERVER, EMAIL_PORT, context=context)
          server.login(msg['From'], password)

          server.sendmail(msg['From'], msg['To'], msg.as_string())
          print("[INFO] Correo enviado exitosamente a {}".format(email_receiver))
          sended_mail = True
     except Exception as e:
          print(e)
          print("[INFO] Correo no enviado ({})".format(email_receiver))
     finally:
          server.quit()
          return sended_mail



#new connection oracle db
conn=cx_Oracle.connect(
          user='',
          password='',
          dsn='192.168.3.XXX:1521/PRDFIT',
          encoding='UTF-8'
     )
# ORACLE
#dsn_tns = cx_Oracle.makedsn('192.168.3.192', '1521', service_name='PRDFIT') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
#conn = cx_Oracle.connect(user='FITC', password='oracle', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'


""" c.execute("select tn.primernombre,tn.segundonombre, tn.apellidopaterno,tn.apellidomaterno,tn.fnacimiento, td.direccion from tpersona tp, tnaturalinformacionbasica tn, tpersonadirecciones td where tp.cpersona=tn.cpersona and tp.cpersona=td.cpersona and tp.ctipopersona='NAT' and tp.cestatuspersona='1'and tp.fhasta>sysdate and tn.fhasta>sysdate and td.fhasta>sysdate and td.ctipodireccion='CE' and EXTRACT(MONTH FROM sysdate)=EXTRACT(MONTH FROM tn.fnacimiento) and EXTRACT(day FROM sysdate)=EXTRACT(day FROM tn.fnacimiento) and not td.direccion LIKE '%xxyz%'") """
c = conn.cursor()
c.execute("select tnib.primernombre, tnib.segundonombre, tnib.apellidopaterno, tnib.apellidomaterno, tnib.fnacimiento, tpd.direccion from tpersona tp, tnaturalinformacionbasica tnib, tpersonadirecciones tpd where tp.cpersona=tnib.cpersona and tpd.cpersona=tnib.cpersona and tp.fhasta>sysdate and tnib.fhasta>sysdate and tpd.fhasta>sysdate and tpd.ctipodireccion='CE' and tp.identificacion='1900107101'")
data = c.fetchall()
conn.close()
# FIN ORACLE

counter = 0
initial_hour = str(datetime.datetime.now()).split(" ")[1][:2]
if len(data) != 0:
     for record in data:
          name_receiver = record[0] + record [1]
          last_name_receiver = record[2] + record [3]
          email_receiver = 'flavio397david@gmail.com'#record[5] 
          ##
          
          ##
          print("--------------------------------------------------")
          print("nombre:", name_receiver, "apellido:", last_name_receiver, "email:", email_receiver)
          try:
               actual_hour = str(datetime.datetime.now()).split(" ")[1][:2]
               if actual_hour == initial_hour and counter < MAX_EMAILS_PER_HOURS: 
                    if email_validation(email_receiver) and send_email(email_receiver, SUBJECT_TO_SEND, html):
                         counter += 1 
                         store_mail_sent_successfully(name_receiver + "," + last_name_receiver + "," + email_receiver)       
                    else:
                         store_error("[EMAIL_ERROR]," + name_receiver + "," + last_name_receiver + "," + email_receiver)
               
               elif actual_hour == initial_hour and counter == MAX_EMAILS_PER_HOURS:
                    actual_minute = str(datetime.datetime.now()).split(" ")[1][3:5]
                    minutes_to_wait = 60 - int(actual_minute)
                    print("minutes_to_wait: ",minutes_to_wait)
                    time.sleep(minutes_to_wait * 60)
                    if email_validation(email_receiver) and send_email(email_receiver, SUBJECT_TO_SEND, CONTENT_TO_SEND):
                         counter = 1 
                         store_mail_sent_successfully(name_receiver + "," + last_name_receiver + "," + email_receiver)
                         initial_hour = str(datetime.datetime.now()).split(" ")[1][:2]       
                    else:
                         store_error("[EMAIL_ERROR]," + name_receiver + "," + last_name_receiver + "," + email_receiver)
               elif actual_hour != initial_hour:
                    initial_hour = actual_hour
                    if email_validation(email_receiver) and send_email(email_receiver, SUBJECT_TO_SEND, CONTENT_TO_SEND):
                         counter = 1 
                         store_mail_sent_successfully(name_receiver + "," + last_name_receiver + "," + email_receiver)
                    else:
                         store_error("[EMAIL_ERROR]," + name_receiver + "," + last_name_receiver + "," + email_receiver)
          except Exception as e:
               print(e)