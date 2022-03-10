from flask import Blueprint, render_template 
from helpers import get_item
import pandas as pd

ticker = Blueprint('ticker', __name__)

@ticker.route('/ticker/<string:ticker>')
@ticker.route('/ticker/<string:ticker>/info')
def view_info(ticker):
   ticker = ticker.upper()
   response = get_item(ticker)
  
   headers = {
        "sector": "Sector:", 
        "industry": "Industry:",
        "website": "Website:",
        "address1": "Address:",  
        "city": "City:",
        "state": "State:",
        "phone": "Phone Number:",
        "zip": "Postcode:",
        "country": "Country:",
    } 
   data = {
       'page_title': 'Ticker Details',
       'ticker': response['Item'],
       
   } 

   return(render_template('info.html', page_data=data, headers=headers))

@ticker.route('/ticker/<string:ticker>/cash_flow')
def view_cash_flow(ticker):
    ticker = ticker.upper()
    response = get_item(ticker)
    cashflow = pd.DataFrame(response['Item']['Cash Flow'])

    data = {
        'page_title': 'Cash Flow',
        'ticker': response['Item'],
    }
    print(cashflow.style)

    return render_template('cash_flow.html', page_data=data, tables=[cashflow.to_html(classes='data', header='true')])

@ticker.route('/ticker/<string:ticker>/balance_sheet')
def view_balance_sheet(ticker):
    ticker = ticker.upper()
    response = get_item(ticker)
    balance_sheet = pd.DataFrame(response['Item']['Balance Sheet'])
    
    data = {
        'page_title': 'Balance Sheet',
        'ticker': response['Item'],
    }
    return render_template('balance_sheet.html', page_data=data, tables=[balance_sheet.to_html(classes='data', header='true')])

@ticker.route('/ticker/<string:ticker>/income_statement')
def view_income_statement(ticker):
    ticker = ticker.upper()

    response = get_item(ticker)
    
    income_statement = pd.DataFrame(response['Item']['Income Statement'])

    data = {
        'page_title': 'Income Statement',
        'ticker': response['Item'],
    }
    return render_template('income_statement.html', page_data=data, tables=[income_statement.to_html(classes='data', header='true')])