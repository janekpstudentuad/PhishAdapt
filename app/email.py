# Import required libraries
from flask_mail import Message

# Import mail lasses from app function
from app import mail

def send_email(subject, sender, recipients, html_body): # add msg.body back to arguments if text option required
    # Instantiate Message object
    msg = Message(subject, sender=sender, recipients=recipients)
    ## Add text email option if email server/client requires
    # msg.body = text_body
    msg.html = html_body
    mail.send(msg)