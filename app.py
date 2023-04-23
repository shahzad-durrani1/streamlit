import streamlit as st
import gspread as gs
import pandas as pd
from google.oauth2 import service_account
import altair as alt



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


# Total Number of Complaints with Closed Status


# % of Timely Responded Complaints

# timely_yes = df.loc[df['timely'] == 'Yes']
# complaints_sum_timely_yes = timely_yes['count of complaint_id'].sum()

# print(complaints_sum_timely_yes)

# print((complaints_sum_timely_yes / complaints_total) * 100)


# Total Number of Complaints with In Progress Status

# response_in_progress = df.loc[df['company_response'] == 'In progress']

# complaints_sum_in_progress = response_in_progress['count of complaint_id'].sum()

# print(complaints_sum_in_progress)

# df_cols = ['complaints_sum', 'complaints_sum_closed', 'complaints_sum_timely_yes', 'complaints_sum_in_progress']
# df_latest = pd.DataFrame(columns=df_cols)


complaints_sum_state = df.groupby('state')['count of complaint_id'].sum()

complaints_sum_state = complaints_sum_state.to_dict()

complaints_sum_state['ALL'] = df['count of complaint_id'].sum()




complaints_closed = df[df['company_response'].str.contains('closed', case=False)]

complaints_closed_state = complaints_closed.groupby('state')['count of complaint_id'].sum()

temp = complaints_closed_state.sum()

complaints_closed_state = complaints_closed_state.to_dict()

complaints_closed_state['ALL'] = temp



timely_complaints = df[df['timely'] == 'Yes'].groupby('state')['count of complaint_id'].sum()

temp = timely_complaints.sum()

complaints_timely_state = timely_complaints.to_dict()

complaints_timely_state['ALL'] = temp 


in_progress_complaints = df[df['company_response'] == 'In progress'].groupby('state')['count of complaint_id'].sum()

temp = in_progress_complaints.sum()

complaints_response_state = in_progress_complaints.to_dict()

complaints_response_state['ALL'] = temp 



# def create_kpi_df(state):
#     print(state)
   
#     if state == 'ALL':
#         print('here')
        
#         df_latest['complaints_sum'] = temp
#         print(df_latest['complaints_sum'])

#         # complaints_closed = df.loc[df['company_response'].str.contains('closed', case=False)]
#         # temp= complaints_closed['count of complaint_id'].sum()
#         # df_latest['complaints_sum_closed'] = temp
        
#         # print(df_latest['complaints_sum_closed'])


#     else:
        

#         # complaints_closed_state = df.loc[(df['state'] == state) & (df['company_response'].str.contains('closed', case=False))]
#         # df_latest['complaints_sum_closed'] = complaints_closed_state['count of complaint_id'].sum()
#         # print(df_latest['complaints_sum_closed'])







# Display the data in a Streamlit table
# st.table(data)
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



# Container 1: KPIs with State Filter

with st.container():
    # Add title and filter widgets
    st.title("KPIs")
    
    
    # Add KPI widgets with placeholder values
    kpi1, kpi2, kpi3, kpi4, state_filter = st.columns([7,7,7,7,5])
    state_filter = st.selectbox(
    'Select a state',
    sorted(state_mapping.keys()))
    # try:
    #     # Try to index the dataframe with the boolean series
    #       create_kpi_df(state_filter)
    # except pd.errors.IndexingError:
    #     # Catch the exception and handle it
    #     print("Error: Unalignable boolean series provided as indexer.")
    
    
    kpi1.metric("Count of Complaints", complaints_sum_state[state_filter])
    kpi2.metric("Complaints with Closed Status", complaints_closed_state[state_filter])
    kpi3.metric("% of Timely Responded Complaints", (complaints_timely_state[state_filter] / complaints_sum_state[state_filter] ) * 100)
    kpi4.metric("Complaints with Closed Status", complaints_response_state[state_filter])



complaints_by_product = df.groupby('product').size().reset_index(name='count')

# Sort the data in descending order of complaint count
complaints_by_product = complaints_by_product.sort_values('count', ascending=False)

# Use Altair to create a horizontal bar chart
chart = alt.Chart(complaints_by_product).mark_bar().encode(
    x='count',
    y=alt.Y('product', sort='-x'),
    color=alt.Color('product', legend=None)
).properties(
    title='Number of Complaints by Product',
    width=800,
    height=500
)

# Display the chart in Streamlit
st.altair_chart(chart)


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
