import smtplib

def sendMailTwo (address, subject, body):
    sender = 'tattar8@doctorattar.com'
    
    message = 'From:  ToolCloud <tattar8@doctorattar.com>\nSubject:  ' + subject + '\n' + body
    try:
        smtp = smtplib.SMTP('doctorattar.com','1337')
        smtp.starttls()
        smtp.login('tattar8','redacted')
        smtp.sendmail(sender,address,message)
    except SMTPException:
        pass
        