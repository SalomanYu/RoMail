# import smtplib
# import os
# import mimetypes
# from email import encoders
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.image import MIMEImage
# from email.mime.audio import MIMEAudio
# from email.mime.application import MIMEApplication
# from email.mime.base import MIMEBase


# def send_email(FROM, TO, PASSWORD, THEME, MESSAGE, attachment={}):
#     sender = FROM
#     password = PASSWORD

#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()

#     # try:
#     #     with open('email_template.html') as file:
#     #         template = file.read()
#     # except IOError:
#     #     error_message = 'ERROR: No such file.'

#     #     return f'\033[2;37;41m {error_message} \033[0;0m'

#     try:
#         server.login(sender, password)
#         msg = MIMEMultipart()
#         msg['Subject'] = THEME
#         msg['From'] = sender
#         msg['To'] = TO

#         for file in attachment:
#             name = attachment[file]
#             ftype, encoding = mimetypes.guess_type(file)
#             file_type, subtype = ftype.split('/')
#             print(file)
#             print(file_type)
#             print(attachment[file])

#             if file_type == 'text':
#                 with open(file) as f:
#                     file = MIMEText(f.read())
#             elif file_type == 'image':
#                 with open(file, 'rb') as f:
#                     file = MIMEImage(f.read(), subtype)
#                     print(file)
#             elif file_type == 'audio':
#                 with open(file, 'rb') as f:
#                     file = MIMEAudio(f.read(), subtype)
#             elif file_type == 'application':
#                 with open(file, 'rb') as f:
#                     file = MIMEApplication(f.read(), subtype)
#             else:
#                 with open(file, 'rb') as f:
#                     file = MIMEBase(file_type, subtype)
#                     file.set_payload(f.read())
#                     encoders.encode_base64(file)

#             # msg.add_header('content-disposition', 'attachment', filename=attachment[name])
#             msg.attach(file)


#         server.sendmail(sender, FROM, msg.as_string())
        
#         success_message = 'The message was send successfully.'
#         return f'\033[3;32;40m {success_message} \033[0;0m'
#     except Exception as error:
#         error_message = f'The program was wrong:\n{error}'

#         return f'\033[2;37;41m {error_message} \033[0;0m'



from re import template
import smtplib
import os
import time
import mimetypes
from tqdm import tqdm
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase


def send_email(FROM, TO, PASSWORD, THEME, MESSAGE, attachment={}):
    sender = FROM
    # your password = "your password"
    password = PASSWORD

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()


    try:
        server.login(sender, password)
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = TO
        msg["Subject"] = THEME

        template = f"""
       <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <img src="https://i.ibb.co/Qk8mBVn/logo-email.png" style='margin-top: -50px;'>
            <p align='center' style='color:#b0d5ee; font: 27px "TeX Gyre Heros Cn"; margin-top: -50px;'>{MESSAGE}</p>
        </body>
        </html>
        """

        msg.attach(MIMEText(template, 'html'))

        print("Collecting...")
        for file in attachment:
            time.sleep(0.4)
            filename = os.path.basename(file)
            ftype, encoding = mimetypes.guess_type(file)
            file_type, subtype = ftype.split("/")
            
            if file_type == "text":
                with open(file) as f:
                    file = MIMEText(f.read())
            elif file_type == "image":
                with open(file, "rb") as f:
                    file = MIMEImage(f.read(), subtype)
            elif file_type == "audio":
                with open(file, "rb") as f:
                    file = MIMEAudio(f.read(), subtype)
            elif file_type == "application":
                with open(file, "rb") as f:
                    file = MIMEApplication(f.read(), subtype)
            else:
                with open(f"attachments/{file}", "rb") as f:
                    file = MIMEBase(file_type, subtype)
                    file.set_payload(f.read())
                    encoders.encode_base64(file)

            file.add_header('content-disposition', 'attachment', filename=filename)
            msg.attach(file)

        server.sendmail(FROM, TO, msg.as_string())
        print('Done')

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


