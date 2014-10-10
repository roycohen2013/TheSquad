from django.core.mail import send_mail
import smtplib
# This is a Python function to send a ToolCloud message to the address (string)
def sendMail (address, subject, body):
    sender = 'thesquad.toolcloud@gmail.com'
    
    #message = EmailMessage('From:  ToolCloud <thesquad.toolcloud@gmail.com>\nSubject:  ' + subject, body, to=[address])
    try:
        #smtp = smtplib.SMTP('smtp.gmail.com:587')
        #smtp.starttls()
        #smtp.login('thesquad.toolcloud','hailthesynergy')
        #smtp.sendmail(sender,address,message)
        send_mail(subject, body, sender,[address], fail_silently = False )
    except smtplib.SMTPException as error:
        #print(error)
        pass
        

