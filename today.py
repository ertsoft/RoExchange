from bs4 import BeautifulSoup
import urllib.request
from pandas import to_datetime
import csv
from tkinter import messagebox


def is_connection(site):
    try:
        urllib.request.urlopen(site, timeout=1)
        return True
    except urllib.error.URLError as Error:
        return False


if is_connection('https://www.bnr.ro/nbrfxrates.xml'):

    req = urllib.request.urlopen('https://www.bnr.ro/nbrfxrates.xml')

    soup = BeautifulSoup(req, 'xml')                         # Install 'lxml' in terminal ! it's a must.

    current_date_tag = soup.find('Cube')
    current_date = current_date_tag['date']

    currency = {}  # initialling a dict that will contain: key=currency and (vale + date )=value
    list_currencies_of_countries = []

    for elem in soup.findAll('Rate'):
        currency[elem['currency']] = elem.decode_contents()
        list_currencies_of_countries.append(elem['currency'])

    current_date_convert = to_datetime(current_date)  # to_datetime - is a func from pandas library
                                                      #  (convert: str -> date)

    """
    To add the today values into the .csv file  
        -creating a list that contain the date and all values of the exchange day 
        -write the list in the .csv file 
    """
    val_l = [current_date]
    for i in list_currencies_of_countries:
        val_l.append(currency[i])

    # Here i take the last date form .csv file:

    with open('currencies(csv)\\currencies2021.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        list_rows = list(csv_reader)  # build a list with all rows from csv_reader (.csv file)

    # take the last day
    last_day_csv = list_rows[len(list_rows)-1]   # take last row (list start from 0 !!)
    last_date_csv = last_day_csv[0]     # take date from last day to compare if it's same with the newest one.

    """
    Verify if we already have the day values in .csv file 
         - if it is there, then do nothing
         - else write the day values in the .csv file 
    """

    if current_date_convert != to_datetime(last_date_csv):
        with open('currencies(csv)\\currencies2021.csv', 'a', newline='') as f_csv:
            f_writer = csv.writer(f_csv, delimiter=',')
            f_writer.writerow(val_l)

    # calculate the diff from last value and previous one:
    last_day_csv = list_rows[len(list_rows)-1]   # take last row (list start from 0 !!)
    day_before_row = list_rows[len(list_rows)-2]
    eur_diff = float(last_day_csv[11]) - float(day_before_row[11])
    usd_diff = float(last_day_csv[29]) - float(day_before_row[29])
else:
    messagebox.showerror('Error to connect', 'There is no internet connection')
