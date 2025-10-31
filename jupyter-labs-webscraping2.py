!pip3 install beautifulsoup4
!pip3 install requests

import sys

import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd

def date_time(table_cells):
    """
    This function returns the data and time from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    """
    This function returns the booster version from the HTML  table cell 
    Input: the  element of a table data cell extracts extra row
    """
    out=''.join([booster_version for i,booster_version in enumerate( table_cells.strings) if i%2==0][0:-1])
    return out

def landing_status(table_cells):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    out=[i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    mass=unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass=mass[0:mass.find("kg")+2]
    else:
        new_mass=0
    return new_mass


def extract_column_from_header(row):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
        
    colunm_name = ' '.join(row.contents)
    
    # Filter the digit and empty names
    if not(colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name    


static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}

import requests

# TASK 1: Request the Falcon9 Launch Wiki page from its URL
response = requests.get(static_url, headers=headers)

from bs4 import BeautifulSoup

# Create a BeautifulSoup object from the HTML response
soup = BeautifulSoup(response.text, 'html.parser')

# Use soup.title attribute
print(soup.title)

# TASK 2: Extract all column/variable names from the HTML table header

# Use table 2 which has the Falcon 9 launch data
falcon9_table = html_tables[2]

# Extract column names
column_names = []
headers = falcon9_table.find_all('th')

for header in headers:
    text = header.get_text(strip=True)
    if text and not text.isdigit():
        column_names.append(text)

print("Final column names:", column_names)

# Let's print the third table and check its content
first_launch_table = html_tables[2]
print(first_launch_table)

# Extract column names using the provided function
column_names = []

# Apply find_all() function with `th` element on first_launch_table
th_elements = first_launch_table.find_all('th')

# Iterate each th element and apply the provided extract_column_from_header() to get a column name
for th in th_elements:
    name = extract_column_from_header(th)
    # Append the Non-empty column name (`if name is not None and len(name) > 0`) into a list called column_names
    if name is not None and len(name) > 0:
        column_names.append(name)

print("Column names extracted:", column_names)

print(column_names)

launch_dict= dict.fromkeys(column_names)

# Remove an irrelvant column
del launch_dict['Date and time ( )']

# Let's initial the launch_dict with each value to be an empty list
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
# Added some new columns
launch_dict['Version Booster']=[]
launch_dict['Booster landing']=[]
launch_dict['Date']=[]
launch_dict['Time']=[]

# Complete the code snippet to fill up the launch_dict with error handling

extracted_row = 0
#Extract each table 
for table_number,table in enumerate(soup.find_all('table',"wikitable plainrowheaders collapsible")):
   # get table row 
    for rows in table.find_all("tr"):
        #check to see if first table heading is as number corresponding to launch a number 
        if rows.th:
            if rows.th.string:
                flight_number=rows.th.string.strip()
                flag=flight_number.isdigit()
        else:
            flag=False
        #get table element 
        row=rows.find_all('td')
        #if it is number save cells in a dictonary 
        if flag and len(row) >= 9:  # Ensure we have enough columns
            extracted_row += 1
            
            # Flight Number value
            launch_dict['Flight No.'].append(flight_number)
            
            # Date and Time
            datatimelist=date_time(row[0])
            date = datatimelist[0].strip(',')
            launch_dict['Date'].append(date)
            time = datatimelist[1]
            launch_dict['Time'].append(time)
              
            # Booster version
            bv=booster_version(row[1])
            if not(bv):
                bv=row[1].a.string if row[1].a else row[1].get_text(strip=True)
            launch_dict['Version Booster'].append(bv)
            
            # Launch Site
            launch_site = row[2].a.string if row[2].a else row[2].get_text(strip=True)
            launch_dict['Launch site'].append(launch_site)
            
            # Payload
            payload = row[3].a.string if row[3].a else row[3].get_text(strip=True)
            launch_dict['Payload'].append(payload)
            
            # Payload Mass
            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)
            
            # Orbit
            orbit = row[5].a.string if row[5].a else row[5].get_text(strip=True)
            launch_dict['Orbit'].append(orbit)
            
            # Customer - Handle None case
            customer_element = row[6].a if row[6].a else row[6]
            customer = customer_element.string if customer_element else row[6].get_text(strip=True)
            launch_dict['Customer'].append(customer)
            
            # Launch outcome
            launch_outcome = list(row[7].strings)[0] if row[7].strings else row[7].get_text(strip=True)
            launch_dict['Launch outcome'].append(launch_outcome)
            
            # Booster landing
            booster_landing = landing_status(row[8])
            launch_dict['Booster landing'].append(booster_landing)

print(f"Extracted {extracted_row} rows")

df= pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items() })

