import streamlit as st
import gspread as gs
import pandas as pd
from google.oauth2 import service_account
import altair as alt
import plotly.express as px



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





# Total Number of Complaints

temp = df[df['state'] == 'AK'].groupby('product')['count of complaint_id'].sum()

temp  = temp.to_dict()

complaints_sum_state = df.groupby('state')['count of complaint_id'].sum()

complaints_sum_state = complaints_sum_state.to_dict()

complaints_sum_state['ALL'] = df['count of complaint_id'].sum()



# Total Number of Complaints with Closed Status

complaints_closed = df[df['company_response'].str.contains('closed', case=False)]

complaints_closed_state = complaints_closed.groupby('state')['count of complaint_id'].sum()

temp = complaints_closed_state.sum()

complaints_closed_state = complaints_closed_state.to_dict()

complaints_closed_state['ALL'] = temp


# % of Timely Responded Complaints
timely_complaints = df[df['timely'] == 'Yes'].groupby('state')['count of complaint_id'].sum()

temp = timely_complaints.sum()

complaints_timely_state = timely_complaints.to_dict()

complaints_timely_state['ALL'] = temp 



# Total Number of Complaints with In Progress Status

in_progress_complaints = df[df['company_response'] == 'In progress'].groupby('state')['count of complaint_id'].sum()

temp = in_progress_complaints.sum()

complaints_response_state = in_progress_complaints.to_dict()

complaints_response_state['ALL'] = temp 



state_mapping = {
    'ALL':'All',
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'DC': 'District of Columbia',
    'FM': 'Federated States of Micronesia',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MH': 'Marshall Islands',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'MP': 'Northern Mariana Islands',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PW': 'Palau',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VI': 'Virgin Islands',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}


# Streamlit app

st.set_page_config(layout="wide")

# Container 1: KPIs with State Filter

with st.container():
    
    # Add title and filter widgets
    st.title("Consumer Financial Complaints Dashboard")
 


    kpi1, kpi2, kpi3, kpi4, state = st.columns([3,3,3,3,3])

    with state:
        state_filter = st.selectbox(
        'Select a state',
        sorted(state_mapping.keys()))
    
     
    if state_filter == 'ALL':
        st.subheader(f"Displaying Data for All States.")
    else:
        st.subheader(f"Displaying Data for {state_mapping[state_filter]}")
    
        
    try:
        kpi1.metric("Count of Complaints", complaints_sum_state[state_filter])
    except KeyError:
        kpi1.metric("Count of Complaints", 'NA')

    try:
        kpi2.metric("Complaints with Closed Status", complaints_closed_state[state_filter])
    except KeyError:
        kpi2.metric("Complaints with Closed Status", 'NA')
    
    try:
        kpi3.metric("Timely Responded Complaints %",  round((complaints_timely_state[state_filter] / complaints_sum_state[state_filter] ) * 100 , 2))
    except KeyError:
        kpi3.metric("Timely Responded Complaints %", 'NA')
    
    try:
        kpi4.metric("Complaints with Closed Status", complaints_response_state[state_filter])
    except KeyError:
        kpi4.metric("Complaints with Closed Status", 'NA')

    
    
    


# Functions to create charts
def create_prod_chart(state):


    if state == 'ALL':
        complaints_by_product = df.groupby('product')['count of complaint_id'].sum().reset_index(name='count')
    else:
        complaints_by_product = df[df['state'] == state].groupby('product')['count of complaint_id'].sum().reset_index(name='count')

    # Sort the data in descending order of complaint count
    complaints_by_product = complaints_by_product.sort_values('count', ascending=False)

    # Use Altair to create a horizontal bar chart
    chart = alt.Chart(complaints_by_product).mark_bar().encode(
    x='count',
    y=alt.Y('product', sort='-x'),
    color=alt.Color('product', legend=None)
    ).properties(
    title='Number of Complaints by Product',
    width=600,
    height=400
    )

    return chart




# Functions to create charts
def create_line_chart(state):
    
    if state == 'ALL':
        complaints_by_month = df.groupby('month_year')['count of complaint_id'].sum().reset_index(name='Number of Complaints')
    else:
        complaints_by_month = df[df['state'] == state].groupby('month_year')['count of complaint_id'].sum().reset_index(name='Number of Complaints')

    chart = alt.Chart(complaints_by_month).mark_line().encode(
    x='month_year',
    y='Number of Complaints'
).properties(
    title='Number of Complaints by Month_Year',
    width=500,
    height=400
    )
        
    return chart
    

# Functions to create charts
def create_pie_chart(state):
    
    if state == 'ALL':
        submitted_via_count = df.groupby('submitted_via')['count of complaint_id'].sum().reset_index(name='Number of Complaints')
        # Create pie chart
        fig = px.pie(submitted_via_count, values=submitted_via_count['Number of Complaints'], names=submitted_via_count['submitted_via'], width = 500 , height=500, title='Number of Complaints by Submitted Via Channel')
    else:
        submitted_via_count = df[df['state'] == state].groupby('submitted_via')['count of complaint_id'].sum().reset_index(name='Number of Complaints')
        fig = px.pie(submitted_via_count, values=submitted_via_count['Number of Complaints'], names=submitted_via_count['submitted_via'], width = 500 , height=500, title='Number of Complaints by Submitted Via Channel')
    
    return fig


# Functions to create charts
def create_tree_map(state):
    if state == 'ALL':
        df_count = df.groupby(['issue', 'sub_issue'])['count of complaint_id'].sum().reset_index(name='Number of Complaints')
        fig  = px.treemap(df_count, path=['issue', 'sub_issue'], values='Number of Complaints', title='Complaints by Issue and Sub-Issue',width=600, height=500)
    else:
        df_count = df[df['state'] == state].groupby(['issue', 'sub_issue'])['count of complaint_id'].sum().reset_index(name='Number of Complaints')
        fig  = px.treemap(df_count, path=['issue', 'sub_issue'], values='Number of Complaints', title='Complaints by Issue and Sub-Issue', width=600, height=500)

    return fig



# Container 2: Two charts side by side
with st.container():
    chart = create_prod_chart(state_filter)
    
    # Add two chart widgets side by side
    chart1, chart2 = st.columns([5,4])

    with chart1:
        st.altair_chart(chart)

    with chart2:
        complaints_by_month = create_line_chart(state_filter)
        st.altair_chart(complaints_by_month)

        

# Container 3: Two charts side by side
with st.container():
    
    # Add two chart widgets side by side
    chart3, chart4 = st.columns([2,2])
   
    with chart3:
        # 
        fig = create_pie_chart(state_filter)
        st.plotly_chart(fig)
    
    with chart4:
        fig = create_tree_map(state_filter)
        st.plotly_chart(fig)
