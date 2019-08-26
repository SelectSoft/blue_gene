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

import pandas as pd
import numpy as np       

import sqlite3

# Scraping the Data

base_data = pd.read_csv("http://tjv.pristupinfo.hr/?sort=1&page=1&download" ,error_bad_lines=False,sep=';',index_col='Rb.')

# Changes the dataType of OIB Column

base_data["OIB"]  = base_data.OIB.fillna(0)
base_data["OIB"] = base_data.OIB.astype(np.int64)

# Changes the column name

base_data.columns = ['entity_name', 'vat_number', 'postal_address', 'zip_code', 'city', 'telephone', 'telefax','website', 'email', 'foi_officer_name', 'foi_officer_telephone','foi_officer_email', 'founder', 'legal_status', 'topics','last_updated']

# Getting the data that is already in a server

server_data = pd.read_csv("https://api.morph.io/SelectSoft/blue_gene/data.csv?key=7hDDGSosf23K7474Bd4P&query=select%20*%20from%20%22data%22",error_bad_lines=False,sep=',')

# Seprating the OIB from tags

# server_data["vat_number"] = server_data['tag_string'].str.extract('(\d+)')

# Changes the dataType of OIB Column

server_data["vat_number"]  = server_data.vat_number.fillna(0)
server_data["vat_number"] = server_data.vat_number.astype(np.int64)

# a = base_data.vat_number.dropna()
# b = server_data.vat_number.dropna()

# a = a.loc[(a!=0)]
# b = b.loc[(b!=0)]

# replace 0 to NaN

server_data['vat_number'] = server_data['vat_number'].replace({ 0:np.nan})
base_data['vat_number'] = base_data['vat_number'].replace({ 0:np.nan})

# Updated    Data that is in both file come in updated 

updatedFlagServer = server_data['vat_number'].isin(base_data['vat_number']) & (server_data['vat_number'].notnull())
updated = server_data[updatedFlagServer]
updatedFlag = base_data['vat_number'].isin(updated['vat_number']) & (updated['vat_number'].notnull())
updated = base_data[updatedFlag]

# Change status to update

updated['status'] = 'updated'

# ab = base_data.vat_number.isin(server_data.vat_number)

# removed
removed = server_data[~updatedFlagServer]
removedflag = base_data['vat_number'].isin(removed['entity_name']) & (removed['entity_name'].notnull())
removed = base_data[removedflag]

removed["vat_number"]  = removed.vat_number.fillna(0)
removed["vat_number"] = removed.vat_number.astype(np.int64)


# Change status to removed

removed['status'] = "removed"

# new

newFlag = base_data['vat_number'].isin(server_data['vat_number'])  & (base_data['vat_number'].notnull())
new = base_data[~newFlag]

# Change status to new

new["status"] = "new"


allData = pd.concat([updated , new, removed]);

# making tags 

# allData["tag_string"] =allData[['legal_status','founder','topics']].values.tolist() 

# changeing object to string 




conn = sqlite3.connect("data.sqlite")

conn.execute("CREATE TABLE if not exists data ('entity_name', 'vat_number', 'postal_address', 'zip_code', 'city', 'telephone', 'telefax','website', 'email', 'foi_officer_name', 'foi_officer_telephone','foi_officer_email', 'founder', 'legal_status', 'topics','last_updated','status')")

allData.to_sql("data", conn, if_exists='replace', index=False)
