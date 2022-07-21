import requests
import json
#!pip3 install folium
#!pip3 install matplotlib

import folium
import os
from bs4 import BeautifulSoup
#import geopandas
from flask import Flask, render_template
app = Flask(__name__)

def getmyIP():
    '''
    This function is going to return the external ip address of
    the user in a string format.
    '''
    url = 'https://whatismyipaddress.com/'
    soup = BeautifulSoup(requests.get(url).text,'html.parser')
    return soup.find_all('span',{'class':'hidden','id':'cf-footer-ip'})[0].text



@app.route('/')
def index():
    ip = getmyIP()
    url = 'http://ip-api.com/json/'+ip
    data = json.loads(requests.get(url).text)
    loc = [data['lat'],data['lon']]
    map_ = folium.Map(location = loc, tiles='OpenStreetMap' , zoom_start = 11)
    folium.Marker(location=loc,popup='Your Location').add_to(map_) 
    map_.save('templates/map.html')
    return render_template('index.html')


@app.route('/map')
def map():
    return render_template('map.html')

if __name__=="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))
 