import xml.etree.ElementTree as ET
import csv

tree = ET.parse('currencies(xml)\\2020_present.xml')  # 2020_present.xml\\2020_present.xml contains all currencies:
root = tree.getroot()  # 2020->present

""" 
i put 'r' mode to block the run. To run the code change in 'a' mode, not in 'w' ('w'-mode have errors)
to use correctly the 'a' follow this protocol:
    - free the .csv file 
    - write the first row (columns name row)
    - after replace 'r' with 'a' in line 15 (this window)
    - is important to have newline='' to avoid the '\n' between rows
"""
with open('currencies(csv)\\currencies.csv', 'r', newline='') as f_csv:  # don t forget to put the correct .csv file !!
    f_writer = csv.writer(f_csv, delimiter=',')

    # initializing a list that will contain: date and all currencies values
    val_l = []

    """
    root[1] = body 
    XML is based on tags , attributes and text 
    .tag -> will return the tag name 
    .attrib -> will return the attribute values as  dictionary
    .text -> will return the text from the tag (more like between tags) 

    after extracting data from XML file , i put all values(date, AED, AUD, etc..) in a list: val_l
    in the end i upload the values from list in the csv fle : currencies.csv (used here csv library) 
    -- list is initialized with 'null' after upload data in csv --
    """

    for line in root[1].findall('Cube'):
        date_attrib_xml = line.attrib
        date = date_attrib_xml['date']
        val_l.append(date)
        for currency in line.findall('Rate'):
            rank = currency.text
            val_l.append(rank)
        f_writer.writerow(val_l)
        val_l = []
