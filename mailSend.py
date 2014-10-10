import smtplib
# This is a Python function to send a ToolCloud message to the address (string)
def sendMail (address, subject, body):
    sender = 'thesquad.toolcloud@gmail.com'
    
    message = 'From:  ToolCloud <thesquad.toolcloud@gmail.com>\nSubject:  ' + subject + '\n' + body
    try:
        smtp = smtplib.SMTP('smtp.gmail.com:587')
        smtp.starttls()
        smtp.login('thesquad.toolcloud','hailthesynergy')
        smtp.sendmail(sender,address,message)
    except SMTPException:
        pass
        

