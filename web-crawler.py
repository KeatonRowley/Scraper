# Collects the links of a given website and aggregates all the links of those links.
# Calculates the frequency of the most linked web pages from the original page. 
# Prints a rating of high and low websites.

import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

def good_url(url):
    if url is None:
        return False
    try:
        r = requests.head(url)
        return r.status_code == 200    
    except requests.exceptions.RequestException as e:  
        return False

def get_website_links(url):
    
    found_urls = []

    if good_url:
        try:
            response = requests.get(url, timeout = 1)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a')

                for link in links:            
                    if good_url(link.get('href')):
                        found_urls.append(link.get('href'))
            else:
                print("url not found")
        except requests.exceptions.RequestException as e:
            print(e)   
        
    return found_urls


def get_website_frequency_dictionary(list):
    website_frequency_dict = {}
    for item in list:
        if item not in website_frequency_dict:
            website_frequency_dict[item] = 1
        else:
            website_frequency_dict[item] += 1
    return website_frequency_dict


def calculate_median_frequency_dict(dict):
    frequencies_list = []
    for item in dict:
        if dict[item] not in frequencies_list:
          frequencies_list.append(dict[item])
    frequencies_list.sort()
    list_length = len(frequencies_list)
    if list_length % 2 == 0:
      return (frequencies_list[int((list_length -1)/2)]+ frequencies_list[int((list_length+1)/2)])/ 2
    else: 
      return frequencies_list[int(list_length/2)]

# returns labelled list of websites as high (greater than the median) or low (less frequent than the median)
def ranked_list_websites(website_frequency_dict, median):
  ranked_list = []
  for website in website_frequency_dict:
    if website_frequency_dict[website] > median:
      ranked_list.append([website, 'high'])
    else:
      ranked_list.append([website, 'low'])
  return ranked_list




#Initial website gathering. 
initial_urls = get_website_links('https://facebook.com')

full_url_list = []


# Get all the links of links of the original webpage.
for initial_url in initial_urls:
    print(initial_url)
    branched_links = get_website_links(initial_url)
   
    for branched_link in branched_links:
        if branched_link is not None:
            full_url_list.append(branched_link)

# calculate each of their frequencies, the median.
website_frequency_dict = get_website_frequency_dictionary(full_url_list)

median = calculate_median_frequency_dict(website_frequency_dict)
ranked_list = ranked_list_websites(website_frequency_dict, median)

# Output high and low websites.
for item in ranked_list:
  if item[1] == 'high':
    print(item)

print('\n')

for item in ranked_list:
  if item[1] == 'low':
    print(item)



