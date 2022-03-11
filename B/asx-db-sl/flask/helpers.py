from flask import session
from app import table
from boto3.dynamodb.conditions import Key
import datetime
import pandas
#################
# H E L P E R S #
#################

def search_db(group, order, page, filters=None, limit=25):
    """ Search the table, returning results sorted by the group and order specified. 

    Args:
        sortBy (str): Which Index to get the data from ['LastUpdatedIndex', 'MarketCapIndex', 'ListingDateIndex', 'GroupIndex', 'NameIndex']
        sortOrder (bool): True for Ascending, False for Descending
        limit (int): number of items to return
    """
    groupDict = {
        'ticker': 'TickerIndex',
        'marketCap': 'MarketCapIndex',
        'companyName': 'NameIndex',
        'group': 'GroupIndex',
        'listingDate': 'ListingDateIndex'
    }
    orderDict = {
        'asc': True,
        'dsc': False
    }
    queryDict = {
        'IndexName': groupDict[group],
        'KeyConditionExpression': Key('GSI1PK').eq('TICKERS'),
        'ScanIndexForward': orderDict[order],
        'Limit': limit
    }
    if page != 1:
        queryDict['ExclusiveStartKey'] = session['pageKey'][f'{int(page)-1}']
    return table.query(**queryDict)

def get_time():
    current_time = datetime.datetime.utcnow().isoformat()
    return current_time

def get_item(ticker):
   response = table.get_item(
       Key={
           'ASX code': ticker
           }
   )
   return(response)

def get_table(data):

    df = pd.DataFrame(data)

    custom_styles = [
        hover(),
        dict(selector="th", props=[("font-size", "100%"),
                                ("text-align", "left")]),
        dict(selector="caption", props=[("caption-side", "bottom")]),
    ]   
    table = df.style.set_properties(**{'max-width': '500px', 'font-size': '10pt'}) \
        .highlight_null(null_color='red') \
        .set_table_attributes('class="table"') \
        .set_table_styles(custom_styles) \
        .render() 
    return table



def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0 else 'black'
    return 'color: %s' % color

def hover(hover_color="#ffff99"):
    return dict(selector="tr:hover",
                props=[("background-color", "%s" % hover_color)])