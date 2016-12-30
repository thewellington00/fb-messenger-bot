
import requests
from lxml import etree

def keystop():
    #xml next bus url
    url = 'http://webservices.nextbus.com/service/publicXMLFeed'

    #set parameters
    # params = {'command': 'routeConfig', 'a': 'sf-muni', 'r': '30'}
    params = {'command': 'predictions', 'a': 'sf-muni', 'r': '30', 'stopId': '14114'}

    #set request headers, gzip according to API guidelines
    headers = {'Accept-Encoding' : 'gzip, deflate'}

    #make request
    r = requests.get(url, params=params, headers=headers)

    xml = etree.fromstring(r.content)
    predictions = xml.xpath('//prediction')

    arrive_times = 'Arrives in '
    for predict in predictions:
        arrive_times = arrive_times + predict.get('minutes') + ', '

    return arrive_times[:-2] + ' minutes'

if __name__ == '__main__':
    print keystop()

