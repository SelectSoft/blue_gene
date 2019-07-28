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


import pandas as pd
import sqlite3

base_data = pd.read_csv("http://tjv.pristupinfo.hr/?sort=1&page=1&download" ,error_bad_lines=False,sep=';',index_col='Rb.')
base_data.columns = ['entity_name', 'vat_number', 'postal_address', 'zip_code', 'city', 'telephone', 'telefax','website', 'email', 'foi_officer_name', 'foi_officer_telephone','foi_officer_email', 'founder', 'legal_status', 'topics','last_updated']

conn = sqlite3.connect("data.sqlite")

conn.execute("CREATE TABLE if not exists data ('entity_name', 'vat_number', 'postal_address', 'zip_code', 'city', 'telephone', 'telefax','website', 'email', 'foi_officer_name', 'foi_officer_telephone','foi_officer_email', 'founder', 'legal_status', 'topics','last_updated')")

base_data.to_sql("data", conn, if_exists='replace', index=False)

