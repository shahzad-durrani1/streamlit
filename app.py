import streamlit as st
import gspread as gs
import pandas as pd
from google.oauth2 import service_account




sheet_url = st.secrets["private_gsheets_url"]

scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

# Set up Google Sheets API credentials
creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes = scopes
)

gc = gs.authorize(creds)

sh = gc.open_by_url(sheet_url)

ws = sh.worksheet('Sheet1')


df = pd.DataFrame(ws.get_all_records())



st.write(df.head(10))
# Load data from a Google Sheets spreadsheet

# sheet_key = sheet_url.split("/")[-2]
# worksheet_name = "Sheet1"  # Replace with the name of your worksheet
# worksheet = client.open_by_key(sheet_key).worksheet(worksheet_name)
# data = worksheet.get_all_values()

# Display the data in a Streamlit table
# st.table(data)
