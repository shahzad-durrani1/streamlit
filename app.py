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



# st.write(df.head(10))

complaints_total = df['count of complaint_id'].sum()

print(complaints_total)

complaints_by_state = df.groupby('state')['count of complaint_id'].sum()

print(complaints_by_state)


# Total Number of Complaints with Closed Status
closed_rows = df.loc[df['company_response'].str.contains('closed', case=False)]

total = closed_rows['count of complaint_id'].sum()

print(total)

# % of Timely Responded Complaints

timely_yes = df.loc[df['timely'] == 'Yes']
complaints_sum_timely_yes = timely_yes['count of complaint_id'].sum()

print(complaints_sum_timely_yes)

print((complaints_sum_timely_yes / complaints_total) * 100)


# Total Number of Complaints with In Progress Status

response_in_progress = df.loc[df['company_response'] == 'In progress']

complaints_sum_in_progress = response_in_progress['count of complaint_id'].sum()

print(complaints_sum_in_progress)




# Load data from a Google Sheets spreadsheet

# sheet_key = sheet_url.split("/")[-2]
# worksheet_name = "Sheet1"  # Replace with the name of your worksheet
# worksheet = client.open_by_key(sheet_key).worksheet(worksheet_name)
# data = worksheet.get_all_values()

# Display the data in a Streamlit table
# st.table(data)



# Container 1: KPIs with State Filter
with st.container():
    # Add title and filter widgets
    st.title("KPIs")
    
    
    # Add KPI widgets with placeholder values
    kpi1, kpi2, kpi3, kpi4, state_filter = st.columns(5)
    with state_filter:
        state_filter = st.selectbox(
    'Select a state',
    sorted(df['state'].unique()))

    with kpi1:
        st.subheader("KPI 1")
        st.write(complaints_by_state[state_filter])
    with kpi2:
        st.subheader("KPI 2")
        st.write("200")
    with kpi3:
        st.subheader("KPI 3")
        st.write("300")
    with kpi4:
        st.subheader("KPI 4")
        st.write("400")
    


# Container 2: Two charts side by side
with st.container():
    # Add title
    st.title("Charts 1 and 2")
    
    # Add two chart widgets side by side
    chart1, chart2 = st.columns(2)
    with chart1:
        st.subheader("Chart 1")
        st.line_chart({"x": [1, 2, 3], "y": [10, 20, 30]})
    with chart2:
        st.subheader("Chart 2")
        st.bar_chart({"x": [1, 2, 3], "y": [10, 20, 30]})

# Container 3: Two charts side by side
with st.container():
    # Add title
    st.title("Charts 3 and 4")
    
    # Add two chart widgets side by side
    chart3, chart4 = st.columns(2)
    with chart3:
        st.subheader("Chart 3")
        st.area_chart({"x": [1, 2, 3], "y": [10, 20, 30]})
    with chart4:
        st.subheader("Chart 4")
        st.line_chart({"x": [1, 2, 3], "y": [10, 20, 30]})


# # Define the state filter dropdown
# state_filter = st.selectbox(
#     'Select a state',
#     sorted(df['state'].unique())
# )

# # Filter the DataFrame by state if a state is selected in the dropdown
# if state_filter:
#     df = df.loc[df['state'] == state_filter]

# # Display the total number of complaints and number of complaints per state
# st.write('### Summary')
# st.write('Total number of complaints:', len(df))
# st.write('Number of complaints in', state_filter, ':', len(df))

# # Display a bar chart of the number of complaints per sub-product in the selected state
# st.write('### Number of complaints per sub-product in', state_filter)
# chart_data = df['sub_product'].value_counts()
# st.bar_chart(chart_data)
