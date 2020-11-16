import json
from scraper import Scraper

def lambda_handler(event, context):
    scrape = Scraper()
    scrape.scrape()  # get info
    scrape.verify()  # sort info
    scrape.store()  # store info
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
lambda_handler('','')