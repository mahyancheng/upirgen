import os
import requests
import pandas as pd
import streamlit as st
from datetime import datetime
from tabulate import tabulate

def get_financial_data(api_key, function, ticker):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": function,
        "symbol": ticker,
        "apikey": api_key,
    }
    response = requests.get(base_url, params=params)
    return response.json()

def filter_last_five_years(data):
    if 'annualReports' not in data:
        return {}

    current_year = datetime.now().year
    five_years_ago = current_year - 5
    filtered_data = [report for report in data['annualReports'] if int(report['fiscalDateEnding'].split("-")[0]) >= five_years_ago]
    return filtered_data

# Example usage

api_key = '6G6DT6CCRO8UWZ39'



def display_valuation(income_statement_data, balance_sheet_data, cash_flow_data):
    # Reverse the data
    income_statement_data = income_statement_data.iloc[::-1]
    balance_sheet_data = balance_sheet_data.iloc[::-1]
    cash_flow_data = cash_flow_data.iloc[::-1]

    headers = ["Metric"] + [date.split("-")[0] for date in income_statement_data['fiscalDateEnding']] + [f"Forecast {i+1}" for i in range(2)]

    # Define the metrics
    metrics = ["Total Revenue", "Gross Profit", "Operating Income", "Net Income"]
    balance_sheet_metrics = ["Total Assets", "Total Liabilities", "Current Assets", "Non-Current Assets", "Current Liabilities", "Non-Current Liabilities"]
    cash_flow_metrics = ["Operating Cash Flow", "Cash Flow from Financing", "Cash Flow from Investment", "Free Cash Flow"]

    # Mapping dictionary for accessing values from the reports
    metric_to_key = {"Total Revenue": "totalRevenue", "Gross Profit": "grossProfit", "Operating Income": "operatingIncome", "Net Income": "netIncome"}
    balance_sheet_metric_to_key = {"Total Assets": "totalAssets", "Total Liabilities": "totalLiabilities", "Current Assets": "totalCurrentAssets", "Non-Current Assets": "totalNonCurrentAssets", "Current Liabilities": "totalCurrentLiabilities", "Non-Current Liabilities": "totalNonCurrentLiabilities"}
    cash_flow_metric_to_key = {"Operating Cash Flow": "operatingCashflow", "Cash Flow from Financing": "cashflowFromFinancing", "Cash Flow from Investment": "cashflowFromInvestment"}

    # Initialize past_data, balance_sheet_past_data, and cash_flow_past_data
    past_data = {metric: [] for metric in metrics}
    balance_sheet_past_data = {metric: [] for metric in balance_sheet_metrics}
    cash_flow_past_data = {metric: [] for metric in cash_flow_metrics}

    for index, report in income_statement_data.iterrows():
        for metric in metrics:
            past_data[metric].append(float(report[metric_to_key[metric]]))

    for index, report in balance_sheet_data.iterrows():
        for metric in balance_sheet_metrics:
            key = balance_sheet_metric_to_key[metric]
            value = float(report[key]) if key in report else 0
            balance_sheet_past_data[metric].append(value)

    for index, report in cash_flow_data.iterrows():
        for metric in cash_flow_metrics[:-1]:  # Exclude "Free Cash Flow"
            cash_flow_past_data[metric].append(float(report[cash_flow_metric_to_key[metric]]))


    # Calculate Free Cash Flow
    cash_flow_past_data["Free Cash Flow"] = [cash_flow_past_data["Operating Cash Flow"][i] + cash_flow_past_data["Cash Flow from Financing"][i] + cash_flow_past_data["Cash Flow from Investment"][i] for i in range(len(cash_flow_past_data["Operating Cash Flow"]))]

    # Calculate forecasted future valuations using CAGR
    for metric in metrics:
        num_years = len(past_data[metric]) - 1
        start_value = past_data[metric][0] if past_data[metric] else 0
        end_value = past_data[metric][-1] if metric in past_data and past_data[metric] else None
        if start_value == 0:
            cagr = 0
        else:
            cagr = (end_value / start_value) ** (1 / num_years) - 1

        forecasted_values = [end_value * (1 + cagr) ** (i + 1) for i in range(2)] if end_value is not None else [None] * 2
        past_data[metric].extend(forecasted_values)

    # Calculate forecasted future valuations using CAGR for the balance sheet
    for metric in balance_sheet_metrics:
        num_years = len(balance_sheet_past_data[metric]) - 1
        start_value = balance_sheet_past_data[metric][0] if balance_sheet_past_data[metric] else 0
        end_value = balance_sheet_past_data[metric][-1] if balance_sheet_past_data[metric] else None
        if start_value == 0:
            cagr = 0
        else:
            cagr = (end_value / start_value) ** (1 / num_years) - 1

        forecasted_values = [end_value * (1 + cagr) ** (i + 1) for i in range(2)]if end_value is not None else [None] * 2
        balance_sheet_past_data[metric].extend(forecasted_values)

    # Calculate forecasted future valuations using CAGR for the cash flow statement
    for metric in cash_flow_metrics:
        num_years = len(cash_flow_past_data[metric]) - 1
        start_value = cash_flow_past_data[metric][0] if cash_flow_past_data[metric] else 0
        end_value = cash_flow_past_data[metric][-1] if cash_flow_past_data[metric] else None
        if start_value == 0:
            cagr = 0
        else:
            cagr = (end_value / start_value) ** (1 / num_years) - 1

        forecasted_values = [end_value * (1 + cagr) ** (i + 1) for i in range(2)]if end_value is not None else [None] * 2
        cash_flow_past_data[metric].extend(forecasted_values)

    # Transpose the income statement data
    transposed_data = [[metric] + values for metric, values in past_data.items()]
    income_statement_df = pd.DataFrame(transposed_data, columns=headers)
    #st.table(income_statement_df)

    # Transpose the balance sheet data
    transposed_balance_sheet_data = [[metric] + values for metric, values in balance_sheet_past_data.items()]
    balance_sheet_df = pd.DataFrame(transposed_balance_sheet_data, columns=headers)
    #st.table(balance_sheet_df)

    # Transpose the cash flow statement data
    transposed_cash_flow_data = [[metric] + values for metric, values in cash_flow_past_data.items()]
    cash_flow_df = pd.DataFrame(transposed_cash_flow_data, columns=headers)
    #st.table(cash_flow_df)
    print(income_statement_data)

    return income_statement_df, balance_sheet_df, cash_flow_df

import yfinance as yf
import pandas as pd

def get_price_change(ticker):
    # Get the data for the stock
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period='1y')

    # Get the data for the S&P 500
    sp500 = yf.Ticker('^GSPC')
    sp500_data = sp500.history(period='1y')

    # Calculate the price change
    stock_data['Price Change'] = stock_data['Close'].pct_change().cumsum()
    sp500_data['Price Change'] = sp500_data['Close'].pct_change().cumsum()


    # Merge the two datasets
    data = pd.DataFrame()
    data[ticker] = stock_data['Price Change']
    data['S&P 500'] = sp500_data['Price Change']

    return data
