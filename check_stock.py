#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import os
import sys
from twilio.rest import Client
import ConfigParser

def main():
    environment = sys.argv[1]
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

    urls = config.get(environment,'urls').split(',')
    #url = "https://www.walmart.com/ip/Funko-POP-Marvel-Stan-Lee-with-Futuristic-Glasses/197736146"
    #url = "https://www.walmart.com/ip/Funko-POP-Marvel-Black-Panther-POP-8-Walmart-Exclusive/446357810"
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        if 'www.walmart.com' in url:
            title = soup.find('h1', 'prod-ProductTitle no-margin heading-a').find('div').get_text()
            button = soup.find('button', class_='prod-ProductCTA--server btn btn-primary btn-block')

        print "Status: " + str(page.status_code)
        print title

        if(button):
            print "Product Available!"
            #os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
            if button.get_text() == 'Add to Cart':
                client.api.account.messages.create(
                    to=to_number,
                    from_=from_number,
                    body="Product Available!\n" + title + '\n' + url)
            else:
                print button.get_text()
        else:
            print "Doesn't seem to be in stock."
        page.connection.close()

    #print soup.prettify()


if __name__ == "__main__":
    main()
