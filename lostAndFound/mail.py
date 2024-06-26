from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from email.mime.image import MIMEImage

def sendMailTo(to,id,d,values):
    subject = "this is subject"
    message = "this is message"
    recipient_list = [to]
    from_email = settings.EMAIL_HOST_USER
    founders = ""
    j = 0
    print(id)
    image_paths = [(f'image{j}','.'+settings.MEDIA_URL+i['image']) for j,i in enumerate(values)]
    print(image_paths)
    for i in values:
        founders += f"""
                <p>Finder's Name : <strong>{i['name']} </strong></p>
                <p> Contact Email : <strong>{i['email']} </strong></p>
                <p>Contact Number : <strong>{i['contact']}</strong></p>
                <p>Description : <strong>{i['description']}</strong>
                <p>Here is the Image of what they have found : </p>
                <p><img src = "cid:image{j}" alt = "Image {j}"></p>"""
        j += 1
    html_content = f"""
        <html>
        <body>
            <p>Dear User,</p>
            <p>We are pleased to inform you that an items matching the description of your {type} <strong> {d} </strong> has been found.</p>
            {founders}
        </body>
        </html>
        """
    msg = EmailMultiAlternatives(subject,message,from_email,recipient_list)
    msg.attach_alternative(html_content,'text/html')

    for cid ,path in image_paths:
        with open(path,'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID',f'<{cid}>')
            msg.attach(img)

            
    msg.send()

    return
