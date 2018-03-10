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
    config.read('/home/ubuntu/project/config.ini')
    urls = config.get(environment,'urls').split(',')

    # items that alread has been alerted
    try:
        with open('alerted.list', 'r') as alertFile:
            alerted = alertFile.readlines()
        alertFile.close()
        alerted = [x.strip() for x in alerted]
    except:
        print "alerted.list not found, will continue."

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
            product = 'walmart_' + soup.find('div', class_='valign-middle s-margin-left copy-mini display-inline-block wm-item-number').get_text().split(':')[1].strip()
        if 'www.target.com' in url:
            title = soup.find('span', attrs={'data-test':'product-title'}).get_text()
            button = soup.find('button', attrs={'data-test':'addToCartBtn'}) #find attribute
            details = soup.find('div', attrs={'data-test':'detailsTab'}).find_all('div')
            for detail in details:
                if 'Item Number (DPCI)' in detail.get_text():
                    product = "target_" + str(detail.get_text().split(':')[1]).strip()

        print title
        print url

        if(button):
            if product not in alerted:
                if button.get_text().lower() == 'add to cart':
                    sendText(environment, config, title, url)
                    print "Product Available!"

                    if os.path.exist('alerted.list'):
                        append_write = 'a'
                    else:
                        append_write = 'w'

                    with open('alerted.list', append_write) as alertFile:
                        alertFile.write(product + "\n")
                    alertFile.close()
                else:
                    print button.get_text()
            else:
                print "Already Alerted! " + product
        else:
            print "Doesn't seem to be in stock."
        page.connection.close()
        print "\n"



if __name__ == "__main__":
    main()
