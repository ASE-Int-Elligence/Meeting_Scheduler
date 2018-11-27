
# Python code to illustrate Sending mail from  
# your Gmail account  
import smtplib 
  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login("chandanapriya12@gmail.com", "") 
  
# message to be sent 
message = "hello"
  
# sending the mail 
s.sendmail("chandanapriya12@gmail.com", "chandanapriya.subscription@gmail.com", message) 
  
# terminating the session 
s.quit() 