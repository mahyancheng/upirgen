

import os
import streamlit as st
from scrape.yahoo_finance_scrape import *
from scrape.google_scrape import *
from scrape.historicaldatascrape import *
from prod.report_section import *

#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
api_key = '6G6DT6CCRO8UWZ39'

def generate_investment_report(ticker, generate_report_section, income_statement_data, balance_sheet_data, cash_flow_data, mosaic_analysis, model ,get_price_change):
    report_parts = []  # Initialize the report_parts list
    st.write(f"Stock price of {ticker} performance compared to S&P500")
    price_change_data = get_price_change(ticker)
    st.line_chart(price_change_data)
    #report_parts.append(get_price_change.to_html())
    st.write("Company Overview")
    st.write(company_overview(generate_report_section, ticker, mosaic_analysis, model))
    #report_parts.append(company_overview(generate_report_section, ticker, mosaic_analysis, model))
    st.write("Industry Analysis")
    st.write(industry_analysis(generate_report_section, ticker, mosaic_analysis, model))
    #report_parts.append(industry_analysis(generate_report_section, ticker, mosaic_analysis, model))
    st.write("Valuation")
    income_statement_df, balance_sheet_df, cash_flow_df = display_valuation(income_statement_data, balance_sheet_data, cash_flow_data)

    st.write("Income Statement:")
    st.table(income_statement_df)
    report_parts.append(income_statement_df.to_html())

    st.write("Balance Sheet:")
    st.table(balance_sheet_df)
    report_parts.append(balance_sheet_df.to_html())

    st.write("Cash Flow Statement:")
    st.table(cash_flow_df)
    report_parts.append(cash_flow_df.to_html())
    st.write("Financial Analysis")
    st.write(financial_analysis(generate_report_section, ticker, income_statement_data, balance_sheet_data, model, calculate_financial_ratios))
    #report_parts.append(financial_analysis(generate_report_section, ticker, income_statement_data, balance_sheet_data, model))
    st.write("Investment Thesis")
    st.write(investment_thesis(generate_report_section, ticker, mosaic_analysis, model))
    #report_parts.append(investment_thesis(generate_report_section, ticker, mosaic_analysis, model))
    st.write("Risk Analysis")
    st.write(risk_analysis(generate_report_section, ticker, mosaic_analysis, model))
    #report_parts.append(risk_analysis(generate_report_section, ticker, mosaic_analysis, model))
    st.write("SWOT Analysis")
    st.write(SWOT_analysis(generate_report_section, ticker, mosaic_analysis, model))
    #report_parts.append(SWOT_analysis(generate_report_section, ticker, mosaic_analysis, model))
    st.write("Investment Recommendations")
    st.write(investment_recommendations_messages(generate_report_section, ticker, mosaic_analysis, model))
    #report_parts.append(investment_recommendations_messages(generate_report_section, ticker, mosaic_analysis, model))
    report = "\n".join(report_parts)
    

def main():
    st.title("Investment Report Generator")
    openai.api_key = st.text_input("Enter the openai api key (gpt-4):")
    ticker = st.text_input("Enter the stock ticker:").upper()
    model = "gpt-3.5-turbo-16k"
    
    if st.button('Generate Report'):
        
        # Scrape Yahoo Finance and Google analysis data
        yahoo_analysis = scrape_yahoo_finance_news(ticker)
        google_analysis = scrape_google_news(ticker)
        bgoogle_analysis = scrape_bgoogle_news(ticker)
        
        
        income_statement_data = pd.DataFrame(filter_last_five_years(get_financial_data(api_key, "INCOME_STATEMENT", ticker)))
        balance_sheet_data = pd.DataFrame(filter_last_five_years(get_financial_data(api_key, "BALANCE_SHEET", ticker)))
        cash_flow_data = pd.DataFrame(filter_last_five_years(get_financial_data(api_key, "CASH_FLOW", ticker)))

   
        # Generate the investment report
        report = generate_investment_report(ticker, generate_report_section, income_statement_data, balance_sheet_data, cash_flow_data, mosaic_analysis, model, get_price_change)

if __name__ == '__main__':
    main()
