import os
import gspread
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# We need both Sheets and Drive scopes to manage files properly
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_gspread_client():
    creds = None
    # Check if token.json exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid creds, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # Authorize gspread with our credentials
    return gspread.authorize(creds)

def manage_sheets():
    gc = get_gspread_client()

    # --- 1. CREATE A NEW SHEET ---
    try:
        sh = gc.create('Python Automation Sheet')
        print(f"Created new sheet: {sh.url}")
    except:
        # If it already exists, just open it
        sh = gc.open('Python Automation Sheet')

    worksheet = sh.get_worksheet(0) # Get the first tab

    # --- 2. WRITE DATA ---
    # Update a single cell
    worksheet.update_acell('A1', 'User Name')
    worksheet.update_acell('B1', 'Email Status')

    # Append a row (Great for logging!)
    worksheet.append_row(['Aryan', 'Sent Successfully'])
    worksheet.append_row(['John Doe', 'Pending'])

    # Write a batch of data
    data_list = [
        ['Alice', 'Sent'],
        ['Bob', 'Failed']
    ]
    worksheet.append_rows(data_list)

    # --- 3. READ DATA ---
    # Get all records as a list of dictionaries
    all_data = worksheet.get_all_records()
    print("\nCurrent Sheet Data:")
    for row in all_data:
        print(row)

    # Get a specific value
    val = worksheet.acell('A2').value
    print(f"\nThe value in A2 is: {val}")

    # --- 4. FORMATTING ---
    # Bold the header row
    worksheet.format("A1:B1", {"textFormat": {"bold": True}})
    
    print("\nSheet Management Complete!")

if __name__ == "__main__":
    manage_sheets()
