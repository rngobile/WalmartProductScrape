#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import os
import sys

def main():
    duration = 0.5  # second
    freq = 440  # Hz
    url = sys.argv[1]
    #url = "https://www.walmart.com/ip/Funko-POP-Marvel-Stan-Lee-with-Futuristic-Glasses/197736146?action=product_interest&action_type=title&beacon_version=1.0.2&bucket_id=irsbucketdefault&client_guid=6fff6954-2964-4a41-397d-70e5234c7ae6&config_id=2&customer_id_enc&findingMethod=p13n&guid=6fff6954-2964-4a41-397d-70e5234c7ae6&item_id=197736146&parent_anchor_item_id=561484083&parent_item_id=561484083&placement_id=irs-2-m2&reporter=recommendations&source=new_site&strategy=PWVUB&visitor_id=btHs8FPjg0c_vEcBhKpfs4"
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
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
        print button.get_text()
    else:
        print "Product does not exists!"

    #print soup.prettify()


if __name__ == "__main__":
    main()
