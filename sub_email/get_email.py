import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os.path import basename
from datetime import datetime

def send_mail(account_path, send_email_data_list: list) -> None:

    with open(account_path,'r') as f:
        secret = {l.split('=')[0].strip(): l.split('=')[1].strip() for l in f.readlines()}
    SMTP_SERVER = secret['host']
    SMTP_PORT = secret['port']
    SMTP_USER = secret['user_id']
    SMTP_PASSWORD = secret['password']

    for target_addr, alarm_time, class_name, high_price, low_price, file_path, total, in send_email_data_list:
            
        if high_price==999999:
            contents = f'''{target_addr}님이 요청하신 {class_name} 중고차 최근 매물 중 {total}대에 관한 정보입니다.'''
        else:
            contents = f'''{target_addr}님이 요청하신 {class_name} 중고차 최근 매물 중 {high_price}만 원과 {low_price}만 원 사이 가격의 매물 {total}대에 관한 정보입니다.'''

        msg = MIMEMultipart('alternative')
        msg['from'] = SMTP_USER
        msg['To'] = target_addr
        msg['Subject'] = f'[중고차 매물 정보] 요청하신 {datetime.today().strftime("%Y%m%d")}일자의 {class_name} 매물 정보입니다.'
        msg.attach(MIMEText(contents))

        email_file = MIMEBase('application', 'vnd.ms.excel')

        with open(file_path, 'rb') as f:
            file_data = f.read()

        email_file.set_payload(file_data)
        encoders.encode_base64(email_file)

        file_name = basename(file_path)
        email_file.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(email_file)

        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.sendmail(SMTP_USER, target_addr, msg.as_string())
        smtp.close()
        # 엑셀 파일 발송 후 제거
        os.remove(file_path)