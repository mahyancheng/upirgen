import openai
import os
from scrape.yahoo_finance_scrape import *
from scrape.google_scrape import *
from scrape.historicaldatascrape import *

# GPT-4 API key
openai.api_key = "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"

# Fetch financial data
ticker = "AAPL"  # Your desired ticker symbol
annual_income_statement, annual_balance_sheet, annual_cash_flow = get_annual_financials(ticker)

# Function to generate report sections
def generate_report_section(section_title, messages):
    gpt4_output = get_gpt4_response(messages)
    print(f"{section_title}:")
    print(gpt4_output)
    print("\n")

# Industry Analysis
industry_analysis_messages = [
    {"role": "system", "content": "You are a hedge fund investment analyst."},
    {"role": "user", "content": f"Provide an industry analysis for {ticker}."},
]
generate_report_section("Industry Analysis", industry_analysis_messages)

# Financial Analysis
financial_analysis_messages = [
    {"role": "system", "content": "You are a hedge fund investment analyst."},
    {"role": "user", "content": f"Perform a financial analysis on {ticker} using the following financial data: {annual_income_statement}, {annual_balance_sheet}, {annual_cash_flow}"},
]
generate_report_section("Financial Analysis", financial_analysis_messages)

# Valuation
def display_valuation(income_statement_data, balance_sheet_data, cash_flow_data):
    # Reverse the income statement data, balance sheet data, and cash flow data
    income_statement_data = list(reversed(income_statement_data))
    balance_sheet_data = list(reversed(balance_sheet_data))
    cash_flow_data = list(reversed(cash_flow_data))

    headers = ["Metric"] + [report['fiscalDateEnding'].split("-")[0] for report in income_statement_data] + [f"Forecast {i+1}" for i in range(2)]
    metrics = ["Total Revenue", "Gross Profit", "Operating Income", "Net Income"]
    balance_sheet_metrics = ["Total Assets", "Total Liabilities", "Current Assets", "Non-Current Assets", "Current Liabilities", "Non-Current Liabilities"]
    cash_flow_metrics = [
        "Operating Cash Flow",
        "Cash Flow from Financing",
        "Cash Flow from Investment",
        "Free Cash Flow",
    ]

    # Mapping dictionary for accessing values from the reports
    metric_to_key = {
        "Total Revenue": "totalRevenue",
        "Gross Profit": "grossProfit",
        "Operating Income": "operatingIncome",
        "Net Income": "netIncome",
    }

    balance_sheet_metric_to_key = {
        "Total Assets": "totalAssets",
        "Total Liabilities": "totalLiabilities",
        "Current Assets": "totalCurrentAssets",
        "Non-Current Assets": "totalNonCurrentAssets",
        "Current Liabilities": "totalCurrentLiabilities",
        "Non-Current Liabilities": "totalNonCurrentLiabilities",
    }

    cash_flow_metric_to_key = {
        "Operating Cash Flow": "operatingCashflow",
        "Cash Flow from Financing": "cashflowFromFinancing",
        "Cash Flow from Investment": "cashflowFromInvestment",
    }

    # Extract the financial data from the income statement
    past_data = {metric: [] for metric in metrics}
    for report in income_statement_data:
        for metric in metrics:
            past_data[metric].append(float(report[metric_to_key[metric]]))

    # Extract the balance sheet data
    balance_sheet_past_data = {metric: [] for metric in balance_sheet_metrics}
    for report in balance_sheet_data:
        for metric in balance_sheet_metrics:
            key = balance_sheet_metric_to_key[metric]
            value = float(report[key]) if key in report else 0
            balance_sheet_past_data[metric].append(value)

     # Extract the financial data for the cash flow statement
    cash_flow_past_data = {metric: [] for metric in cash_flow_metrics[:-1]}  # Exclude "Free Cash Flow"
    for report in cash_flow_data:
        for metric in cash_flow_metrics[:-1]:  # Exclude "Free Cash Flow"
            cash_flow_past_data[metric].append(float(report[cash_flow_metric_to_key[metric]]))

    # Calculate Free Cash Flow
    cash_flow_past_data["Free Cash Flow"] = [
        cash_flow_past_data["Operating Cash Flow"][i] +
        cash_flow_past_data["Cash Flow from Financing"][i] +
        cash_flow_past_data["Cash Flow from Investment"][i]
        for i in range(len(cash_flow_past_data["Operating Cash Flow"]))
    ]
     # Calculate forecasted future valuations using CAGR for the balance sheet
    for metric in balance_sheet_metrics:
        num_years = len(balance_sheet_past_data[metric]) - 1
        start_value = balance_sheet_past_data[metric][0]
        end_value = balance_sheet_past_data[metric][-1]
        if start_value == 0:
            cagr = 0
        else:
            cagr = (end_value / start_value) ** (1 / num_years) - 1

        forecasted_values = [end_value * (1 + cagr) ** (i + 1) for i in range(2)]
        balance_sheet_past_data[metric].extend(forecasted_values)

     # Calculate forecasted future valuations using CAGR for the cash flow statement
    for metric in cash_flow_metrics:
        num_years = len(cash_flow_past_data[metric]) - 1
        start_value = cash_flow_past_data[metric][0]
        end_value = cash_flow_past_data[metric][-1]
        if start_value == 0:
            cagr = 0
        else:
            cagr = (end_value / start_value) ** (1 / num_years) - 1

        forecasted_values = [end_value * (1 + cagr) ** (i + 1) for i in range(2)]
        cash_flow_past_data[metric].extend(forecasted_values)

    # Transpose the income statement data
    transposed_data = [[metric] + values for metric, values in past_data.items()]

    # Display the income statement data in a tabulated format
    print("Income Statement:")
    print(tabulate(transposed_data, headers=headers, tablefmt="grid"))

    # Transpose the balance sheet data
    transposed_balance_sheet_data = [[metric] + values for metric, values in balance_sheet_past_data.items()]

    # Display the balance sheet data in a tabulated format
    print("\nBalance Sheet:")
    print(tabulate(transposed_balance_sheet_data, headers=headers, tablefmt="grid"))

    # Transpose the cash flow statement data
    transposed_cash_flow_data = [[metric] + values for metric, values in cash_flow_past_data.items()]

    # Display the cash flow statement data in a tabulated format
    print("\nCash Flow Statement:")
    print(tabulate(transposed_cash_flow_data, headers=headers, tablefmt="grid"))


# Investment Thesis
investment_thesis_messages = [
    {"role": "system", "content": "You are a hedge fund investment analyst."},
    {"role": "user", "content": f"Provide an investment thesis for {ticker}."},
]
generate_report_section("Investment Thesis", investment_thesis_messages)

# Risk Analysis
risk_analysis_messages = [
    {"role": "system", "content": "You are a hedge fund investment analyst."},
    {"role": "user", "content": f"Perform a risk analysis on {ticker}."},
]
generate_report_section("Risk Analysis", risk_analysis_messages)

# Investment Recommendations
investment_recommendations_messages = [
    {"role": "system", "content": "You are a hedge fund investment analyst."},
    {"role": "user", "content": f"Provide investment recommendations for {ticker}."},
]
generate_report_section("Investment Recommendations", investment_recommendations_messages)
