import openai
import os
from tabulate import tabulate
from scrape.yahoo_finance_scrape import *
from scrape.google_scrape import *
from scrape.historicaldatascrape import *
import pandas as pd

# GPT-4 API key
#openai.api_key = "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"
#api_key = '6G6DT6CCRO8UWZ39'


# Function to generate report sections
def generate_report_section(section_title, messages,model):
    gpt4_output = get_gpt4_response(model,messages)
    print(f"{section_title}:")
    print(gpt4_output)
    print("\n")
    return gpt4_output

def mosaic_analysis(generate_report_section, ticker, yahoo_analysis, google_analysis,bgoogle_analysis ,model):
    mosaic_analysis_messages = [
        {"role": "system", "content": "You are a hedge fund investment analyst."},
        {"role": "user", "content": f"Generate a combined mosaic analysis for {ticker} using Yahoo Finance analysis: {yahoo_analysis} and Google analysis: {google_analysis} and bGoogle analysis: {bgoogle_analysis}. Think step by step and stitch them up together using mosaic analysis."},
    ]
    generate_report_section("Mosaic Analysis", mosaic_analysis_messages,model)
    return generate_report_section("Mosaic Analysis", mosaic_analysis_messages,model)

# Company Overview
def company_overview(generate_report_section,ticker,mosaic_analysis,model):
    company_overview_messages = [
    {"role": "system", "content": "You are a hedge fund investment analyst."},
    {"role": "user", "content": f"Provide an company overview for {ticker}, using the following data {mosaic_analysis}, write only company overview, do not write other things other than that"},
    ]   
    generate_report_section("Company Overview", company_overview_messages,model)
    return generate_report_section("Company Overview", company_overview_messages,model)

# Industry Analysis
def industry_analysis(generate_report_section,ticker,mosaic_analysis,model):
    industry_analysis_messages = [
    {"role": "system", "content": "You are a hedge fund investment analyst."},
    {"role": "user", "content": f"Provide an industry analysis for {ticker}, using the following data {mosaic_analysis},write only industry analysis, do not write other things other than that. Do not apologise, do not write context which makes it look like an unprofessional report."},

    ]
    generate_report_section("Industry Analysis", industry_analysis_messages,model)
    return generate_report_section("Industry Analysis", industry_analysis_messages,model)

# Valuation

def calculate_financial_ratios(income_statement_data, balance_sheet_data):
    def to_float(value):
        return 0.0 if value is None or value == 'None' else float(value)

    current_assets = to_float(balance_sheet_data.iloc[-1]['totalCurrentAssets'])
    current_liabilities = to_float(balance_sheet_data.iloc[-1]['totalCurrentLiabilities'])

    inventory = to_float(balance_sheet_data.iloc[-1]['inventory'])
    quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities != 0 else None

    long_term_debt = to_float(balance_sheet_data.iloc[-1]['longTermDebt'])
    short_term_debt = to_float(balance_sheet_data.iloc[-1]['shortTermDebt'])
    total_debt = long_term_debt + short_term_debt

    total_assets = to_float(balance_sheet_data.iloc[-1]['totalAssets'])
    debt_ratio = total_debt / total_assets if total_assets != 0 else None

    ebit = to_float(income_statement_data.iloc[-1]['operatingIncome'])
    interest_expense = to_float(income_statement_data.iloc[-1]['interestExpense'])
    interest_coverage_ratio = ebit / interest_expense if interest_expense != 0 else None

    return {
        "Quick Ratio": quick_ratio,
        "Debt Ratio": debt_ratio,
        "Interest Coverage Ratio": interest_coverage_ratio,
    }


# Financial Analysis
def financial_analysis(generate_report_section, ticker, income_statement_data, balance_sheet_data, model, calculate_financial_ratios):
    financial_ratios = calculate_financial_ratios( income_statement_data, balance_sheet_data)
    
    financial_analysis_messages = [
        {"role": "system", "content": "You are a hedge fund investment analyst."},
        {"role": "user", "content": f"Perform a financial analysis on {ticker} financial ratios using data from the calculated financial ratios: {financial_ratios}, write only financial analysis, do not write other things other than that"},
    ]
    generate_report_section("Financial Analysis", financial_analysis_messages,model)
    return     generate_report_section("Financial Analysis", financial_analysis_messages,model)


# Investment Thesis
def investment_thesis(generate_report_section,ticker,mosaic_analysis,model):
    investment_thesis_messages = [
    {"role": "system", "content": "You are a hedge fund investment analyst."},
    {"role": "user", "content": f"Provide an investment thesis for {ticker}, using the following data {mosaic_analysis},write only investment thesis, do not write other things other than that"},    
    ]
    generate_report_section("Investment Thesis", investment_thesis_messages,model)
    return     generate_report_section("Investment Thesis", investment_thesis_messages,model)


# Risk Analysis
def risk_analysis(generate_report_section,ticker,mosaic_analysis,model):
    risk_analysis_messages = [
    {"role": "system", "content": "You are a hedge fund investment analyst."},
    {"role": "user", "content": f"Perform a risk analysis on {ticker}, using the following data {mosaic_analysis},write only risk analysis, do not write other things other than that. Do not apologise, do not write context which makes it look like an unprofessional report.your risk analysis should be based on {mosaic_analysis}."},
    
    ]
    generate_report_section("Risk Analysis", risk_analysis_messages,model)
    return    generate_report_section("Risk Analysis", risk_analysis_messages,model)

# SWOT Analysis    
def SWOT_analysis(generate_report_section,ticker,mosaic_analysis,model):
    SWOT_analysis_messages = [
    {"role": "system", "content": "You are a hedge fund investment analyst."},
    {"role": "user", "content": f"Perform a SWOT analysis on {ticker}, using the following data {mosaic_analysis}, write only SWOT analysis, do not write other things other than that"},
    
    ]
    generate_report_section("Risk Analysis", SWOT_analysis_messages,model)
    return      generate_report_section("Risk Analysis", SWOT_analysis_messages,model)

# Investment Recommendations
def investment_recommendations_messages(generate_report_section,ticker,mosaic_analysis,model):
    investment_recommendations_messages = [
    {"role": "system", "content": "You are a hedge fund investment analyst."},
    {"role": "user", "content": f"Provide investment recommendations for {ticker}, using the following data {mosaic_analysis},write only Investment Recommendations with relevant reasons and points to point out why to buy or sell and what to take note about the company, do not write other things other than that"},
    ]
    generate_report_section("Investment Recommendations", investment_recommendations_messages,model)
    return     generate_report_section("Investment Recommendations", investment_recommendations_messages,model)
