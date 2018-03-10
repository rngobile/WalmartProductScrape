#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import os
import sys
from twilio.rest import Client
import ConfigParser

def main():
    environment = 'TRIAL'
    # Get variables from config file
    config = ConfigParser.ConfigParser()
    config.read('../config.ini')

    # variables for message beeps
    duration = 0.5  # second
    freq = 440  # Hz

    # twilio send message
    account_sid = config.get(environment,'account_sid')
    auth_token = config.get(environment,'auth_token')
    to_number = config.get(environment,'to_number')
    from_number = config.get(environment,'from_number')
    client = Client(account_sid, auth_token)

    url = sys.argv[1]
    #url = "https://www.walmart.com/ip/Funko-POP-Marvel-Stan-Lee-with-Futuristic-Glasses/197736146"
    #url = "https://www.walmart.com/ip/Funko-POP-Marvel-Black-Panther-POP-8-Walmart-Exclusive/446357810"
    page = requests.get(url)

    print "Status: " + str(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())
    #stock = soup.find('span', class_='copy-mini')
    #print(stock.get_text())
    title = soup.find('h1', 'prod-ProductTitle no-margin heading-a').find('div').get_text()
    button = soup.find('button', class_='prod-ProductCTA--server btn btn-primary btn-block')
    print title

    if(button):
        print "Product Exist!"
        #os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
        client.api.account.messages.create(
            to=to_number,
            from_=from_number,
            body=title)
        print button.get_text()
    else:
        print "Product does not exists!"

    #print soup.prettify()


if __name__ == "__main__":
    main()
