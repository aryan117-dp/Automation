import os.path
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# 'gmail.send' allows the script to send emails on your behalf.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return creds

def send_automated_email(creds, to_email, subject, body_text):
    """Sends an email via the Gmail API."""
    try:
        # Build the Gmail service
        service = build('gmail', 'v1', credentials=creds)

        # Construct the email message
        message = EmailMessage()
        message.set_content(body_text)
        message['To'] = to_email
        message['From'] = 'me' # 'me' is a special keyword for the authenticated user
        message['Subject'] = subject

        # Encode the message in base64 URL-safe format
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}

        # Send the message
        send_message = service.users().messages().send(
            userId="me", 
            body=create_message
        ).execute()
        
        print(f'Success! Message Id: {send_message["id"]}')

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    # 1. Authenticate and get credentials
    credentials = authenticate_gmail()
    
    # 2. Define your email parameters
    recipient = "sarrafaryan550@gmail.com"  # Change this to a real email address
    email_subject = "Automated Python Report"
    email_body = "Hello! This email was sent automatically using Python and the Gmail API."
    
    # 3. Send the email
    send_automated_email(credentials, recipient, email_subject, email_body)
