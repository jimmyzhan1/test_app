import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"
st.header("Monthly spending breakdown")

df2 = pd.read_csv('Apple Card Transactions - June 2022.csv')
# Dataset is now stored in a Pandas Dataframe
df2

# Sort rows by transaction and clearing dates
df2["Transaction Date"] = pd.to_datetime(df2["Transaction Date"])
df2["Clearing Date"] = pd.to_datetime(df2["Clearing Date"])
df2 = df2.sort_values(by=["Transaction Date", "Clearing Date"])
df2 = df2.reset_index(drop=True)
df2["Type"].unique()

# Only keeping Purchase, Credit, and Debit transactions
list1 = ['Purchase', 'Credit', 'Debit']
df3 = df2[df2["Type"].isin(list1)]
df3 = df3.reset_index(drop=True)
df3

# Cum Sum for transactions
df3['Cum (USD)'] = df3["Amount (USD)"].cumsum()
df3

# Line plot
fig0 = px.line(df3,
               x='Transaction Date',
               y='Amount (USD)',
               color='Purchased By',
               markers=True,
               hover_name='Purchased By',
               hover_data=["Merchant"],
               height=400,
               width=1200)
fig1 = px.line(df3,
               x='Transaction Date',
               y='Cum (USD)',
               markers=True,
               hover_name='Purchased By',
               hover_data=["Merchant"],
               height=400,
               width=1200)

st.plotly_chart(fig0)
st.plotly_chart(fig1)

# Dictionary is now stored in a Pandas Dataframe
dff = pd.read_csv('Transact_dict_csv.csv')
dff

# Replace Category value based on keyword from Dictionary
for i in range(len(dff)):
  ind = df3[df3['Description'].str.contains(dff['Keyword'][i])].index
  df3.loc[ind, "Category"] = dff.loc[i, "Category"]

df3

# Group by category
df = df3.groupby(["Category",
                  "Purchased By"])['Amount (USD)'].sum().reset_index()
df
total = df['Amount (USD)'].sum()
total
fig2 = px.bar(df,
              x="Category",
              y="Amount (USD)",
              color='Purchased By',
              barmode='group',
              title='Sum = $' + str(total))
fig3 = px.pie(df, values='Amount (USD)', names='Category')

st.plotly_chart(fig2)
st.plotly_chart(fig3)
