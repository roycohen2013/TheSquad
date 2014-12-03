from django.core.mail import send_mail
import smtplib
# This is a Python function to send a ToolCloud message to the address (string)

EMAIL_ENABLED = True

def sendMail (address, subject, body):
    if EMAIL_ENABLED:
        sender = 'toolbot@toolcloud.me'
        
        #message = EmailMessage('From:  ToolCloud <thesquad.toolcloud@gmail.com>\nSubject:  ' + subject, body, to=[address])
        try:
            #smtp = smtplib.SMTP('smtp.gmail.com:587')
            #smtp.starttls()
            #smtp.login('thesquad.toolcloud','hailthesynergy')
            #smtp.sendmail(sender,address,message)
            send_mail(subject, body, sender,[address], fail_silently = True )
        except smtplib.SMTPException as error:
            #print(error)
            pass
    else:
        print("Email notifications are disabled.")
        
        
        

