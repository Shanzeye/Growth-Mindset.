
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Custom CSS to style the Streamlit app
st.markdown("""
    <style>
        /* Set background color for the entire page */
        body {
            background-color: #FFF0F5;  /* Light Pink */
            font-family: 'Arial', sans-serif;
        }

        /* Title Styling */
        h1 {
            color: #FF6347;  /* Tomato */
            text-align: center;
            font-size: 40px;
        }

        h2 {
            color: #FF6347;  /* Tomato */
            text-align: center;
            font-size: 30px;
        }

        /* Sidebar Styling */
        .css-1d391kg {  /* Sidebar selector */
            background-color: #FF6347;
            color: white;
        }

        /* Button Styling */
        button {
            background-color: #FF6347;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            cursor: pointer;
        }

        button:hover {
            background-color: #FF4500;  /* Orange Red */
        }

        /* Input Field Styling */
        .stTextInput, .stNumberInput, .stSelectbox, .stDateInput {
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }

        /* Graph Styling */
        .matplotlib-plot {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Table Styling */
        table {
            border-collapse: collapse;
            width: 100%;
        }

        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        th {
            background-color: #FF6347;  /* Tomato */
            color: white;
        }

    </style>
""", unsafe_allow_html=True)

# Define expense categories
categories = ['Food', 'Rent', 'Transportation', 'Entertainment', 'Utilities', 'Others']

# Initialize or load expense data from session state
def initialize_expenses_data():
    if 'df' not in st.session_state:
        # If data doesn't exist, create a new empty dataframe
        data = {category: [] for category in categories}
        data['Date'] = []
        data['Description'] = []
        st.session_state.df = pd.DataFrame(data)

# Function to add an expense entry
def add_expense(df, category, amount, date, description):
    new_entry = {category: amount, 'Date': date, 'Description': description}
    for cat in categories:
        if cat != category:
            new_entry[cat] = 0
    new_entry_df = pd.DataFrame([new_entry])
    return pd.concat([df, new_entry_df], ignore_index=True)

# Function to calculate total expenses and savings
def calculate_totals(df, total_budget):
    total_spent = df[categories].sum().sum()
    total_savings = total_budget - total_spent
    return total_spent, total_savings

# Function to get category-wise expenses
def get_category_expenses(df):
    return df[categories].sum()

# Function to get pie chart data
def get_pie_chart_data(df):
    pie_data = df[categories].sum()
    pie_data = pie_data[pie_data > 0]  # Remove categories with zero expenses
    return pie_data

# Function to plot category expenses as a bar chart
def plot_category_expenses(category_expenses):
    fig, ax = plt.subplots()
    category_expenses.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title("Expenses by Category")
    ax.set_ylabel("Amount Spent ($)")
    ax.set_xlabel("Categories")
    st.pyplot(fig)

# Function to plot expense distribution as a pie chart
def plot_expense_distribution(pie_data):
    fig2, ax2 = plt.subplots()
    ax2.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle
    ax2.set_title("Expense Distribution by Category")
    st.pyplot(fig2)

# Function to display the expense table
def display_expenses(df):
    st.header("All Expenses")
    st.write(df)

# Function to filter expenses by date
def filter_by_date(df, start_date, end_date):
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    return filtered_df

# Function to download expenses as CSV
def download_data(df):
    csv = df.to_csv(index=False)
    st.download_button(label="Download Expenses as CSV", data=csv, file_name="expenses.csv", mime="text/csv")

# Function to display monthly summary
def monthly_summary(df):
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_expenses = df.groupby('Month')[categories].sum()
    st.header("Monthly Summary")
    st.write(monthly_expenses)

# Initialize the DataFrame on app start
initialize_expenses_data()

# Streamlit UI
st.title("Interactive Personal Expense Tracker")
st.markdown("<h2 style='text-align: center; color: #FF6347;'>Track your spending & savings</h2>", unsafe_allow_html=True)

# User input for total budget
st.sidebar.header("Set Your Budget")
total_budget = st.sidebar.number_input("Enter your total budget for the month", min_value=0.0, step=0.01)

# Expense entry form
st.header("Enter Your Expenses")
category = st.selectbox("Select Expense Category", categories)
amount = st.number_input(f"Enter amount for {category}", min_value=0.0, step=0.01)
description = st.text_input(f"Enter a short description for the expense")
date = st.date_input("Enter the Date")

# Button to add expense
if st.button("Add Expense"):
    if amount > 0:
        st.session_state.df = add_expense(st.session_state.df, category, amount, date, description)
        st.success(f"Added {amount} to {category} for {date} with description: {description}")
    else:
        st.error("Amount should be greater than zero.")

# Display total expenses and savings
if total_budget > 0:
    st.header("Total Spending & Savings")
    total_spent, total_savings = calculate_totals(st.session_state.df, total_budget)
    st.write(f"Total Budget: ${total_budget:.2f}")
    st.write(f"Total Amount Spent: ${total_spent:.2f}")
    st.write(f"Total Amount Saved: ${total_savings:.2f}")
else:
    st.warning("Please enter your total budget.")

# Display category-wise expenses as a bar chart
category_expenses = get_category_expenses(st.session_state.df)
plot_category_expenses(category_expenses)

# Display a pie chart for the overall spending distribution
pie_data = get_pie_chart_data(st.session_state.df)
if not pie_data.empty:
    plot_expense_distribution(pie_data)
else:
    st.warning("No expenses recorded yet for a pie chart.")
