from django.core.mail import send_mail
from PhoneDotCom import sendText
import smtplib
# This is a Python function to send a ToolCloud message to the address (string)

EMAIL_ENABLED = False
TEXT_ENABLED = True

doNotReply = "\n\nPlease do not reply to this message."

def sendMail (recipientProfile, subject, body):
    if EMAIL_ENABLED:
        if recipientProfile.emailNotifs:
            sender = 'toolbot@toolcloud.me'
            greeting = "Hi " + recipientProfile.user.first_name + ", \n\n"
            adios =  "\n\nCheers, \n\nThe Squad"
            content = greeting + body + adios + doNotReply
            #message = EmailMessage('From:  ToolCloud <thesquad.toolcloud@gmail.com>\nSubject:  ' + subject, body, to=[address])
            try:
                #smtp = smtplib.SMTP('smtp.gmail.com:587')
                #smtp.starttls()
                #smtp.login('thesquad.toolcloud','hailthesynergy')
                #smtp.sendmail(sender,address,message)
                send_mail(subject, content, sender,[recipientProfile.user.email], fail_silently = True )
            except smtplib.SMTPException as error:
                #print(error)
                pass
    else:
        print("Email notifications are disabled.")
    if TEXT_ENABLED:
        if recipientProfile.textNotifs:
            greeting = "Hey " + recipientProfile.user.first_name + ", "
            adios = " - Your friendly neighborhood ToolBot"
            content = greeting + body + adios
            sendText(recipientProfile.phoneNumber, content)
    else:
        print("Text notifications are disabled.")
        
        
        

