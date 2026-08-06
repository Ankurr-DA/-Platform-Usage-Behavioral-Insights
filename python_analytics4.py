# -----------------------------------------------------------------------------
# LOAD SQL VIEWS INTO PANDAS DATAFRAMES
# -----------------------------------------------------------------------------
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

USER = 'root'
PASSWORD = 'ankur'  
HOST = 'localhost'
PORT = '3306'
DATABASE = 'sql_analytics4' 

engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

#importing views from SQL
sql_query1 = 'select * from v_transactions;'
sql_query2 = 'select * from v_app_activity;'

df_transactions = pd.read_sql(sql_query1, con=engine)
df_activity = pd.read_sql(sql_query2, con=engine)

# -----------------------------------------------------------------------------
# 1. CLEANING DF_TRANSACTIONS
# -----------------------------------------------------------------------------

# Fixing age_group
a = {'18_25': '18-25', '18 - 25': '18-25',
    '26_40': '26-40', '26 - 40': '26-40',
    '41_60': '41-60', '41 - 60': '41-60',
    '60 +': '60+', '60_plus': '60+'}
df_transactions['age_group'] = df_transactions['age_group'].fillna('Unknown')
df_transactions['age_group'] = df_transactions['age_group'].str.strip()
df_transactions['age_group'] = df_transactions['age_group'].replace(a)

# Fixing region
b = {'N':'NORTH','S':'SOUTH','E':'EAST','W':'WEST'}
df_transactions['region'] = df_transactions['region'].fillna('UNASSIGNED')
df_transactions['region'] = df_transactions['region'].str.upper().str.strip()
df_transactions['region'] = df_transactions['region'].replace(b)

# Fixing payment_channel
df_transactions['payment_channel'] = df_transactions['payment_channel'].fillna('UNCLASSIFIED_CHANNEL')
df_transactions['payment_channel'] = df_transactions['payment_channel'].str.upper().str.strip()
df_transactions['payment_channel'] = df_transactions['payment_channel'].str.replace('_',' ')

# Fixing transaction_amount
df_transactions['transaction_amount'] = df_transactions['transaction_amount'].str.replace('Rs.','')
df_transactions['transaction_amount'] = df_transactions['transaction_amount'].str.replace(',','')
df_transactions['transaction_amount'] = pd.to_numeric(df_transactions['transaction_amount'],errors='coerce')
df_transactions['transaction_amount'] = df_transactions['transaction_amount'].fillna(0)
df_transactions = df_transactions[df_transactions['transaction_amount'] > 0]

# Fixing transaction_status
df_transactions['transaction_status'] = df_transactions['transaction_status'].fillna('UNKNOWN')
df_transactions['transaction_status'] = df_transactions['transaction_status'].str.upper().str.strip()
df_transactions['transaction_status'] = df_transactions['transaction_status'].str.replace('_',' ')

# Fixing transaction_timestamp
df_transactions['transaction_timestamp'] = pd.to_datetime(df_transactions['transaction_timestamp'],dayfirst=False,format='mixed',errors='coerce')

# -----------------------------------------------------------------------------
# 2. CLEANING DF_ACTIVITY
# -----------------------------------------------------------------------------

# Fixing channel_type
df_activity['channel_type'] = df_activity['channel_type'].str.upper().str.strip()
df_activity['channel_type'] = df_activity['channel_type'].str.replace('_',' ')

# Fixing action_performed
df_activity['action_performed'] = df_activity['action_performed'].str.upper().str.strip()
df_activity['action_performed'] = df_activity['action_performed'].str.replace('_',' ')
df_activity.dropna(subset='action_performed',inplace=True)

# Fixing event_timestamp
df_activity['event_timestamp'] = pd.to_datetime(df_activity['event_timestamp'],dayfirst=False,format='mixed',errors='coerce')
df_activity.dropna(subset='event_timestamp',inplace=True)

# Merged the dataframes into one
merged_df = pd.merge(df_transactions,df_activity,on='customer_id',how='left')
mapping = {
    'UPI': 'MOBILE APP',
    'IMPS': 'MOBILE APP',
    'NEFT': 'NET BANKING',
    'BILL PAY': 'NET BANKING'
}
merged_df['channel_type'] = merged_df['channel_type'].fillna(merged_df['payment_channel'].map(mapping))
merged_df.dropna(subset='channel_type',inplace=True)

# Report 1--------------------------------------------------------------------------------------
# Extract Hour for peak hour analysis
merged_df['hour'] = merged_df['event_timestamp'].dt.hour
merged_df['peak_hour'] = pd.cut(
    merged_df['hour'],
    bins=[-1, 6, 12, 18, 24],
    labels=['Night (00-06)', 'Morning (06-12)', 'Afternoon (12-18)', 'Evening (18-24)']
)
# Find total action count
total = merged_df.groupby(['channel_type', 'action_performed']).agg(
    total_actions=('customer_id', 'count')
).reset_index()

# Find the peak time
window_counts = merged_df.groupby(['channel_type', 'action_performed', 'peak_hour']).size().reset_index(name='window_count')
peak = window_counts.sort_values('window_count', ascending=False).drop_duplicates(
    subset=['channel_type', 'action_performed']
)[['channel_type', 'action_performed', 'peak_hour']]

# Merge the totals with the peak time
report1 = pd.merge(total, peak, on=['channel_type', 'action_performed'])

# Calculate activity share percentage
total_platform_actions = report1['total_actions'].sum()
report1['activity_share'] = ((report1['total_actions'] / total_platform_actions) * 100).round(2)
report1['activity_share'] = report1['activity_share'].map('{}%'.format)

# Save the report in excel format
report1.to_excel('Event_Action_Analysis.xlsx',index=False)
print('Event_Action_Analysis.xlsx Exported Successfully')


# Report 2--------------------------------------------------------------------------------------
# Calculate failed & success transaction status & Amount
total_platform_actions = report1['total_actions'].sum()
merged_df['failed'] = merged_df['transaction_status'] != 'SUCCESS'
merged_df['failed_amount'] = merged_df['transaction_amount'].where(merged_df['failed'], 0)
merged_df['success'] = merged_df['transaction_status'] == 'SUCCESS'
merged_df['settled_amount'] = merged_df['transaction_amount'].where(merged_df['success'], 0)

# Group by the dataframe
report2 = merged_df.groupby(['channel_type', 'payment_channel']).agg(
    total_transactions=('customer_id', 'count'),
    passed_transactions=('success', 'sum'),
    failed_transactions=('failed', 'sum'),
    settled_volume=('settled_amount', 'sum'),
    volume_at_risk=('failed_amount', 'sum')
).reset_index()

# Calculate success_rate
report2['success_rate'] = ((report2['passed_transactions'] / report2['total_transactions']) * 100).round(2)
report2['success_rate'] = report2['success_rate'].map('{}%'.format)

# Save the report in excel format
report2.to_excel('Transaction_Performance.xlsx',index=False)
print('Transaction_Performance.xlsx Exported Successfully')


