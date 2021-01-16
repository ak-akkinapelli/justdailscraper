from bs4 import BeautifulSoup
import urllib
import urllib.request
import requests
import csv

def innerHTML(element):
    return element.decode_contents(formatter="html")

def get_name(body):
  return body.find('span', {'class':'jcn'}).a.string

def get_img(body):
  return body.find('div', {'class':'thumb_img'}).img["data-src"]

def get_address(body):
  return body.find('span', {'class':'mrehover'}).text.strip()


page_number = 1
service_count = 1

fields = ['Name','img','AddressLine1','AddressLine2']
out_file = open('tailors.csv','w')
csvwriter = csv.DictWriter(out_file,fieldnames=fields,extrasaction='ignore', delimiter=',')


while True:
  # Check if reached end of result
  if page_number > 2:
    break

  url="https://www.justdial.com/Hyderabad/Tailors/nct-10470248"
  print(url)
  req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}) 
  page = urllib.request.urlopen( req )

  soup = BeautifulSoup(page.read(), "html.parser")
  services = soup.find_all('li', {'class': 'cntanr'})

  # Iterate through the 10 results in the page
  for service_html in services:

    # Parse HTML to fetch data     
    dict_service = {}
    name = get_name(service_html)
    print(name);
    address = get_address(service_html)
    if name != None:
      dict_service['Name'] = name
    if address != None:
        seq =address.split(',')
        AddressLine1, *AddressLine2 = seq
        dict_service['AddressLine1'] = AddressLine1
        dict_service['AddressLine2'] = AddressLine2
    img = get_img(service_html)
    dict_service['img'] = img
    # Write row to CSV
    csvwriter.writerow(dict_service)

    print("#" + str(service_count) + " " , dict_service)
    service_count += 1

  page_number += 1

out_file.close()
