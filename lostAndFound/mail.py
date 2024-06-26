import smtplib
from email.message import EmailMessage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
from django.conf import settings

def sendMailTo(reporter,values):
    sender = 'greviencevvit@gmail.com'
    password = 'pvhr wbrs tmbv rxty '
    subject = "Found Item Notification"
    receiver = reporter.email
    type = reporter.submissionID.split('_')[0]
    founders = ""
    image_paths = ['.'+settings.MEDIA_URL+i['image'] for i in values]
    print(image_paths)
    j = 0
    for i in values:
        founders += f"""
                <p>Finder's Name : {i['name']} </p>
                <p> Contact Email : {i['email']} </p>
                <p>Contact Number : {i['contact']}</p>
                <p>Here is the Image of what they have found : </p>
                <p><img src = "cid:image{j}" alt = "Image {j}"></p>
"""
        j += 1
        
    html_content = f"""
        <html>
        <body>
            <p>Dear User,</p>
            <p>We are pleased to inform you that an items matching the description of your {type} "{reporter.description}" has been found.</p>
            {founders}
        </body>
        </html>
        """
    mail = EmailMessage()
    mail['from'] = sender
    mail['to'] = receiver
    mail['subject'] = subject
    mail.add_attachment(MIMEText(html_content,'html'))
    context = ssl.create_default_context()
    if len(image_paths) != 0:
        for idx, image_path in enumerate(image_paths):
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                image_name = image_path.split('/')[-1]
                image_cid = f'image{idx + 1}'
                mime_image = MIMEImage(image_data, name=image_name)
                mime_image.add_header('Content-ID', f'<{image_cid}>')
                mime_image.add_header('Content-Disposition', 'inline', filename=image_name)
                mail.add_attachment(mime_image)

    with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
        smtp.login(sender,password)
        smtp.sendmail(sender,receiver,mail.as_string())
    return 

