import http.server 
import socketserver 
import json 
import pandas as pd 
import requests
import time 
import sqlite3 
import random 
import os 
import hashlib 
import pprint 

#defining a HTTP request Handler class 

class ServiceHandler(http.server.SimpleHTTPRequestHandler): 
    
    def do_GET(self): 
        
        if self.path == '/': 
            self.send_response(200)
            self.send_header('Context-type', 'text/json') 
            self.end_headers() 

             
    url="https://restcountries.com/v3.1/all"
    url_countries_by_region="https://restcountries.com/v3.1/region/{region}"

    headers = {
				'x-rapidapi-key': "921cfc17abmsh42834139575656fp12725cjsn8ce3ad10333d",
				'x-rapidapi-host': "restcountries-v1.p.rapidapi.com"
				}

    regions_data = []
    hash_languages =[]
    countries = []
    times=[]
    data  = json.loads(requests.request("GET", url, headers=headers).text)
    
    for region_info in data: 
        
        if region_info['region']: 
            if not region_info['region'] in regions_data: 
                regions_data.append(region_info['region'])
    
    for regions in regions_data: 
        start_time=time.time()
        countries_data=json.loads(requests.request("GET", url_countries_by_region.format(region=regions),
        headers=headers
        ).text) 
        random_number=random.randint(0,len(countries_data)-1)
        countries.append(countries_data[random_number]["name"]["common"])
        hash_languages.append(countries_data[random_number]['languages'])
        end_time=time.time()
        times.append(round((end_time-start_time)*1000,2))
    
    languages=[]
    for valor in hash_languages: 
        languages.append(list(valor.values()))
    
    values_languages=[]

    for valor in languages: 

        if len(valor)==1: 
            values_languages.append(hashlib.sha1(valor[0].encode()).hexdigest())
        else: 
            count=random.randint(0, len(valor)-1)
            values_languages.append(hashlib.sha1(valor[count].encode()).hexdigest()) 

    
   
    
    table=pd.DataFrame() 
    table["Region"]=regions_data
    table["Country"]=countries
    table["Languages"]=values_languages
    table["Times"]=times
   
    

    print(table)


    

class ReuseAddrTCPServer(socketserver.TCPServer): 
    allow_reuse_address: True 

PORT=8000

myserver=ReuseAddrTCPServer(("", PORT), ServiceHandler) 
myserver.daemon_threads=True 
print(f"http://127.0.0.1:{PORT}")

try: 
    myserver.serve_forever()
except: 
    print("closing the server")
    myserver.server_close()
   
