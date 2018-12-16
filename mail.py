import smtplib

def send_email(subject, msg, to):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("ticketz.ticket.info@gmail.com", "Ticketz123.")
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail("ticketz.ticket.info@gmail.com", to, message)
        server.quit()
    except:
        print("fail: email send")
