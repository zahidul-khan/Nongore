#importing all librabies
import requests
import pandas as panda
import matplotlib.pyplot as pyPlot
from urllib import urlencode

#function definations
def custom2_main():
    print "Begin Execution"

    #get access token
    url = 'https://api.yelp.com/oauth2/token'
    data = urlencode({
        'client_id': '2iAU5SNZAcRkVXv78A9qEQ',
        'client_secret': 'zq0jtYIzFcSACANpv3CTcEHItJsSaAHquQTQ9HcALVFwGYa1G8AUv1JsvvSoobxS',
        'grant_type': 'client_credentials',
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }

    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']

    #make query
    search_limit = 50   #does not work if more than 50 is set. return 20 values if nothing is set
    url = 'https://api.yelp.com/v3/businesses/search'
    url_params = {
        'term': 'breakfast_brunch +',
        'location': 'Helsinki +',
        'limit': search_limit
    }
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }
    response = requests.request('GET', url, headers=headers, params=url_params).json()

    #get businesses
    businesses = response.get('businesses')
    dataArray = []
    for business in businesses:
        business_id = business['id']
        name = business['name']
        review_count = business['review_count']
        price = business.get('price', None)
        rating = business['rating']
        distance  = business['distance']

        #str = "%s   %s  %d  %s  %f  %f"%(business_id, name, review_count, price, rating, distance)
        #print str      #checking information

        #get individual business information for business hours
        inner_url = 'https://api.yelp.com/v3/businesses/'+business_id
        inner_response = requests.request('GET', inner_url, headers=headers, params=None).json()

        hours= inner_response.get('hours')
        if(hours == None):
            continue    #continue if no hours information is available
            #end if
        open_at_weekend = False
        saturday = False
        sunday = False
        for open in hours[0]['open']:
            day = open['day']
            if(day == 5):
                saturday = True
                #end if
            if(day == 6):
                sunday = True
                #end if
            if(saturday == True and sunday == True):
                open_at_weekend = True
                #end if
            #end for
        #check and add in array
        if(review_count>=5 and len(price)<=4 and open_at_weekend == True):
            data = {}
            data['id'] = business_id
            data['name'] = name
            data['review_count'] = review_count
            data['price'] = len(price)
            data['rating'] = rating
            data['distance'] = distance
            dataArray.append(data)
            #end if
        #end for

    #show output
    sortedDataArray = sorted(dataArray, key=lambda distance: distance)
    sortedDataArray = sorted(sortedDataArray, key=lambda price: price)
    sortedDataArray = sorted(sortedDataArray, key=lambda rating: rating, reverse=True)
    sortedDataArray = sorted(sortedDataArray, key=lambda review_counts: review_counts, reverse=True)
    top5 = sortedDataArray[:5]  #get the top 5
    print top5

    #plot
    dataFrame = panda.DataFrame(top5, columns=['name', 'rating', 'price', 'review_count'])
    dataFrame.set_index('name', inplace=True)
    panda.set_option('display.max_colwidth', -1)
    print dataFrame
    dataFrame.plot()
    pyPlot.show()

    #end of custom2_main()


#execution
custom2_main()