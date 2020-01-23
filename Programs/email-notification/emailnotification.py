from picamera import PiCamera
from time import sleep
import smtplib
import email
camera = PiCamera()
camera.start_preview()
sleep(2)
camera.capture('/home/pi/home_secure_system/Programs/email-notification/image.jpg')
sleep(2)
camera.stop_preview()
camera.close()
#E-mail notification kuldese
def send_an_email():  
    toaddr = 'gyorvaripeter1996@gmail.com'      # To id 
    me = '2labamkozottnagyobb@gmail.com'          # your id
    subject = "!!!!!HOME SECURE SYSTEM ALERT!!!!!"              # Subject
  
    msg = MIMEMultipart()  
    msg['Subject'] = subject  
    msg['From'] = me  
    msg['To'] = toaddr  
    msg.preamble = "Az iment ez a szemely csengetett. "   
    #msg.attach(MIMEText(text))  
  
    part = MIMEBase('application', "octet-stream")  
    part.set_payload(open("image.jpg", "rb").read())  
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment; filename="image.jpg"')   # File name and format name
    msg.attach(part)  
  
    try:  
       s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
       s.ehlo()  
       s.starttls()  
       s.ehlo()  
       s.login(user = '2labamkozottnagyobb@gmail.com', password = 'p1e2t3e4r5')  # User id & password
       #s.send_message(msg)  
       s.sendmail(me, toaddr, msg.as_string())  
       s.quit()  
    #except:  
    #   print ("Error: unable to send email")    
    except SMTPException as error:  
          print ("Error")                # Exception
send_an_email()