#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".


# import pandas as pd
# import sqlite3

# base_data = pd.read_csv("http://tjv.pristupinfo.hr/?sort=1&page=1&download" ,error_bad_lines=False,sep=';',index_col='Rb.')
# base_data.columns = ['entity_name', 'vat_number', 'postal_address', 'zip_code', 'city', 'telephone', 'telefax','website', 'email', 'foi_officer_name', 'foi_officer_telephone','foi_officer_email', 'founder', 'legal_status', 'topics','last_updated']

# conn = sqlite3.connect("data.sqlite")

# conn.execute("CREATE TABLE if not exists data ('entity_name', 'vat_number', 'postal_address', 'zip_code', 'city', 'telephone', 'telefax','website', 'email', 'foi_officer_name', 'foi_officer_telephone','foi_officer_email', 'founder', 'legal_status', 'topics','last_updated')")

# base_data.to_sql("data", conn, if_exists='replace', index=False)


# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 14:28:26 2019

@author: Saifullah
@email: saifullah.alam552@gmail.com
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 01:10:23 2019

@author: Saifullah
"""

import pandas as pd
import numpy as np       
import os
import sqlite3
import re
import validators
import dateutil.parser as parser

# Scraping the Data
def isValidEmail(email):
 if len(email) > 7:
  if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?))$", email) != None:
   return True
 return False

def isValidWebsite(web):
    if not validators.url('http://'+web):
        return False
    return True

def dateConvertor(date):
    new_date = parser.parse(date)
    return new_date.isoformat()

base_data = pd.read_csv("http://tjv.pristupinfo.hr/?sort=1&page=1&download",converters={'OIB': lambda x: str(x)} ,error_bad_lines=False,sep=';',index_col='Rb.')

# Making multiple columns 


# Changes the dataType of OIB Column

base_data["OIB"] =base_data.OIB.astype('str')

base_data['OIB'] = base_data['OIB'].replace({'':np.nan})

base_data = base_data.dropna(subset=['OIB'])
base_data = base_data.drop_duplicates(subset=['OIB'], keep=False)
# Changes the column name

base_data.columns = ['entity_name', 'vat_number', 'postal_address', 'zip_code', 'city', 'telephone', 'telefax','website', 'email', 'foi_officer_name', 'foi_officer_telephone','foi_officer_email', 'founder', 'legal_status', 'topics','last_updated']



base_data["email"] = base_data.email.fillna('')
base_data["foi_officer_email"] = base_data.foi_officer_email.fillna('')
base_data["website"] = base_data.website.fillna('')

try:
    base_data[['email','email_1','email_2','email_3']] = pd.DataFrame(base_data.email.str.split(';',expand=True))
except:
  try:
       base_data[['email','email_1','email_2']] = pd.DataFrame(base_data.email.str.split(';',expand=True))
  except:
      try:
          base_data[['email','email_1']] = pd.DataFrame(base_data.email.str.split(';',expand=True))
      except:
          base_data['email'] = pd.DataFrame(base_data.email.str.split(';',expand=True))
          
          
try:
    base_data[['foi_officer_email','foi_officer_email_1','foi_officer_email_2','foi_officer_email_3']] = pd.DataFrame(base_data.foi_officer_email.str.split(';',expand=True))
except:
  try:
       base_data[['foi_officer_email','foi_officer_email_1','foi_officer_email_2']] = pd.DataFrame(base_data.foi_officer_email.str.split(';',expand=True))
  except:
      try:
          base_data[['foi_officer_email','foi_officer_email_1']] = pd.DataFrame(base_data.foi_officer_email.str.split(';',expand=True))
      except:
          base_data['foi_officer_email'] = pd.DataFrame(base_data.foi_officer_email.str.split(';',expand=True))
          
try:
    base_data[['website','website_1','website_2','website_3']] = pd.DataFrame(base_data.website.str.split(';',expand=True))
except:
  try:
       base_data[['website','website_1','website_2']] = pd.DataFrame(base_data.website.str.split(';',expand=True))
  except:
      try:
          base_data[['website','website_1']] = pd.DataFrame(base_data.website.str.split(';',expand=True))
      except:
          base_data['website'] = pd.DataFrame(base_data.website.str.split(';',expand=True))
          
    
base_data["email"] = base_data.email.fillna(np.nan)
base_data["foi_officer_email"] = base_data.foi_officer_email.fillna(np.nan)
base_data["website"] = base_data.website.fillna(np.nan)     

# Getting the data that is already in a server
my_secret_value = os.environ['MORPH_MYSECRET']
server_data = pd.read_csv("https://api.morph.io/SelectSoft/blue_gene/data.csv?key="+my_secret_value+"&query=select%20*%20from%20%22data%22",converters={'vat_number': lambda x: str(x)},error_bad_lines=False,sep=',')

server_data["vat_number"] =server_data.vat_number.astype('str')
# Seprating the OIB from tags

base_data = base_data.reset_index()
base_data = base_data.drop({'Rb.'},1)

server_data = server_data.reset_index()
server_data = server_data.drop({'index'},1)
# server_data["vat_number"] = server_data['tag_string'].str.extract('(\d+)')

# Changes the dataType of OIB Column


# a = base_data.vat_number.dropna()
# b = server_data.vat_number.dropna()

# a = a.loc[(a!=0)]
# b = b.loc[(b!=0)]

# replace 0 to NaN


# Updated    Data that is in both file come in updated 

updatedFlagServer = base_data['vat_number'].isin(server_data['vat_number']) & (server_data['vat_number'].notnull())
updated = base_data[updatedFlagServer]
#updatedFlag = base_data['vat_number'].isin(updated['vat_number']) & (updated['vat_number'].notnull())
#updated = base_data[updatedFlag]

# Change status to update

updated['status'] = 'updated'

# ab = base_data.vat_number.isin(server_data.vat_number)

# removed
removedflag = base_data['vat_number'].isin(server_data['vat_number'])
removed = base_data[~removedflag]




# Change status to removed

removed['status'] = "removed"

# new

newFlag = base_data['vat_number'].isin(server_data['vat_number'])  & (base_data['vat_number'].notnull())
new = base_data[~newFlag]

# Change status to new

new["status"] = "created"


allData = pd.concat([updated , new, removed]);

#allData['vat_number'] = allData['vat_number'].astype(str).replace('\.0', '', regex=True)

# making tags 

# allData["tag_string"] =allData[['legal_status','founder','topics']].values.tolist() 

# changeing object to string 


allData = allData.drop_duplicates(subset=['vat_number'], keep=False)

allData['email_validation_pass'] = ""
allData['website_validation_pass'] = ""
allData['foi_officer_email_validation_pass'] = ""
allData = allData.reset_index()
for x in range(len(allData)):
    if(isValidEmail(allData['email'][x]) and allData['email'][x] ):
        allData['email_validation_pass'][x] = "true"
    elif(not allData['email'][x]):
        allData['email_validation_pass'][x] = "nan"
    else:
        allData['email_validation_pass'][x] = "fail"
        
    if(isValidEmail(allData['foi_officer_email'][x]) and allData['foi_officer_email'][x]):
        allData['foi_officer_email_validation_pass'][x] = "true"
    elif(not allData['foi_officer_email'][x]):
        allData['foi_officer_email_validation_pass'][x] = "nan"
    else:
        allData['foi_officer_email_validation_pass'][x] = "fail"
        
    if(isValidWebsite(allData['website'][x]) and allData['website'][x]):
        allData['website_validation_pass'][x]= "true"
    elif(not allData['website'][x]):
        allData['website_validation_pass'][x] = "nan"
    else:
        allData['website_validation_pass'][x] = "fail"
        if(not pd.isnull(allData['last_updated'][x])):
            allData['last_updated'][x] = dateConvertor(allData['last_updated'][x])

conn = sqlite3.connect("data.sqlite")

conn.execute("CREATE TABLE if not exists data ('entity_name', 'vat_number', 'postal_address', 'zip_code', 'city', 'telephone', 'telefax','website', 'email', 'foi_officer_name', 'foi_officer_telephone','foi_officer_email', 'founder', 'legal_status', 'topics','last_updated','status')")

allData.to_sql("data", conn, if_exists='replace', index=False)




