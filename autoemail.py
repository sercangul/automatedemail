import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

#------------------------------------------------------------------------------
port = 587 
smtp_server = "smtp.gmail.com"
login = "*******@gmail.com" 
password = "*********" 

subject = "GAIN 2021 at UT Austin - Registration Open - February 25,2021"
sender_email = "******@gmail.com"

message = MIMEMultipart()
message["From"] = sender_email
message["Subject"] = subject
#------------------------------------------------------------------------------
filename = "GAIN2021_Corporate_Package.pdf"
# We assume that the file is in the directory where you run your Python script from
with open(filename, "rb") as attachment:
    # The content type "application/octet-stream" means that a MIME attachment is a binary file
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode to base64
encoders.encode_base64(part)

# Add header 
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)
#------------------------------------------------------------------------------
df = pd.read_csv('2021_contact_list_for_script.csv') 

#df = pd.read_csv('script-test.csv') 

#------------------------------------------------------------------------------
for index, row in df.iterrows():
    Name = row['Name']
    Company = row['Company']
    email = row['Email']
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["Subject"] = subject
    message["To"] = email
    
    body = "Dear %s \n \nThe Graduate Engineering Council (GEC) welcomes you to our first virtual GAIN (Graduate and Industry Networking) event since its inception in 2004. GAIN facilitates connections between employers and our outstanding graduate students through student presentations, industry talks, and a career fair.\n\nIf you would like to learn more about the cutting-edge research conducted at UT Austin, as well as recruit some of the brightest graduate engineers in the nation, then this event is for you. GAIN 2021 will be held virtually on February 25, 2021! Registration is now open, and we would love to have %s participate.\n\nPlease see the links below to access the itinerary, the updated corporate package with pricing, and the registration. \nItinerary: https://sites.utexas.edu/gain/about/itinerary/  \nCorporate package: https://sites.utexas.edu/gain/home/partnership/ \nRegistration: https://tinyurl.com/yyrzdpy3 \n\nSince the event will be virtual, our expenses will also be lower. Therefore, there is a good discount on sponsorship prices compared to previous years.\nYou can find more about GAIN through our website at https://sites.utexas.edu/gain/. \n\nSincerely, \nSheila Gerardo & Sercan Gul \nGAIN Co-Directors, 2021 \nGAIN Website: https://sites.utexas.edu/gain/ "   % (Name, Company)    
    message.attach(MIMEText(body, "plain"))
    
    # Open PDF file in binary mode
    # Add attachment to your message and convert it to string
    message.attach(part)
    text = message.as_string()
    # send your email
    with smtplib.SMTP(smtp_server,port) as server:
        server.connect("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(login, password)
        server.sendmail(sender_email, email, text)
        server.quit()
        print(index, email)
