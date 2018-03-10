#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import os
import sys
from twilio.rest import Client
import ConfigParser

def sendText(environment, config, title, url):
    # twilio send message
    account_sid = config.get(environment,'account_sid')
    auth_token = config.get(environment,'auth_token')
    to_number = config.get(environment,'to_number')
    from_number = config.get(environment,'from_number')
    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
        to=to_number,
        from_=from_number,
        body="Product Available!\n" + title + '\n' + url)

def beep():
    duration = 0.5 #seconds
    freq = 440 # Hz
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))

def writeFile(writeMe):
    #writeFile(soup.prettify("utf-8"))
    with open("output.log", "w") as file:
        file.write(str(writeMe))

def main():
    environment = sys.argv[1]

    # Get variables from config file
    config = ConfigParser.ConfigParser()
    config.read('../config.ini')
    urls = config.get(environment,'urls').split(',')

    for url in urls:
        try:
            page = requests.get(url)
        except:
            print "Website is down: " + url + "\n"
            continue

        soup = BeautifulSoup(page.content, 'html.parser')

        if 'www.walmart.com' in url:
            title = soup.find('h1', 'prod-ProductTitle no-margin heading-a').find('div').get_text()
            button = soup.find('button', class_='prod-ProductCTA--server btn btn-primary btn-block')
        if 'www.target.com' in url:
            title = soup.find('span', attrs={'data-test':'product-title'}).get_text()
            button = soup.find('button', attrs={'data-test':'addToCartBtn'}) #find attribute

        print title
        print url

        if(button):
            print "Product Available!"
            if button.get_text().lower() == 'add to cart':
                sendText(environment, config, title, url)
            else:
                print button.get_text()
        else:
            print "Doesn't seem to be in stock."
        page.connection.close()
        print "\n"



if __name__ == "__main__":
    main()
