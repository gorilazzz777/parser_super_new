import logging
import smtplib
import os
import mimetypes
import traceback
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from time import sleep

from app.settings import MAIL_ADDR_FROM, MAIL_PASSWORD, MAIL_MSG_SUBJ, MAIL_MSG_TEXT

logger = logging.getLogger("app")


class MailSender():

    def __init__(self):
        self.mail_addr_from = MAIL_ADDR_FROM
        self.mail_password = MAIL_PASSWORD
        self.server = self.get_server()

    def get_server(self):
        server = None
        for i in range(10):
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Создаем объект SMTP
                break
            except:
                sleep(120)
        if server:
            server.login(self.mail_addr_from, self.mail_password)
        return server

    def attach_file(self, msg, filepath):  # Функция по добавлению конкретного файла к сообщению
        filename = os.path.basename(filepath)  # Получаем только имя файла
        ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
        if ctype is None or encoding is not None:  # Если тип файла не определяется
            ctype = 'application/octet-stream'  # Будем использовать общий тип
        maintype, subtype = ctype.split('/', 1)  # Получаем тип и подтип
        if maintype == 'text':  # Если текстовый файл
            with open(filepath) as fp:  # Открываем файл для чтения
                file = MIMEText(fp.read(), _subtype=subtype)  # Используем тип MIMEText
                fp.close()  # После использования файл обязательно нужно закрыть
        elif maintype == 'image':  # Если изображение
            with open(filepath, 'rb') as fp:
                file = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
        elif maintype == 'audio':  # Если аудио
            with open(filepath, 'rb') as fp:
                file = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
        else:  # Неизвестный тип файла
            with open(filepath, 'rb') as fp:
                file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
                file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
                fp.close()
                encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
        file.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(file)

    def process_attachement(self, msg, files):
        for f in files:
            if os.path.isfile(f):
                self.attach_file(msg, f)
            elif os.path.exists(f):
                dir_mail = os.listdir(f)
                for file in dir_mail:
                    self.attach_file(msg, f + "/" + file)

    def send_email(self, addr_to, files, subject=None):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.mail_addr_from
            msg['To'] = addr_to
            msg['Subject'] = MAIL_MSG_SUBJ if subject is None else subject
            body = MAIL_MSG_TEXT
            msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст
            self.process_attachement(msg, files)
            server = self.get_server()
            server.send_message(msg)
            server.quit()
            return True
        except:
            logger.error(f'Error in send_email: {traceback.format_exc()}')
            return False
