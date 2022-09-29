from rightmove_webscraper import RightmoveData
import time
from playsound import playsound
import pandas as pd

url = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E475&maxBedrooms=2&minBedrooms=2&maxPrice=1500&minPrice=700&propertyTypes=&maxDaysSinceAdded=1&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords="
data = RightmoveData(url).get_results
data.drop(['search_date'], axis=1, inplace=True)
pd.options.display.max_colwidth = 1000
while True:
    time.sleep(60)
    newdata = RightmoveData(url).get_results
    newdata.drop(['search_date'],axis=1,inplace=True)
    bothdata = pd.concat([data,newdata],axis=0)
    bothdata.drop_duplicates(inplace=True,ignore_index=True,keep=False)
    cols = bothdata.columns
    bothdata = bothdata.merge(data,on=['url'],how='left')
    bothdata = bothdata[bothdata.price_y.isnull()]
    if bothdata.size != 0:
        playsound('ding.mp3')
        print(bothdata.url.to_string())
    else:
        t = time.localtime()
        current_time = time.strftime("%H:%M", t)
        print("No new properties at " + current_time)
    data = newdata

