import sys
import csv
import datetime
import requests

def call_api(startdate, enddate, filename):
    url = 'http://real-chart.finance.yahoo.com/table.csv'
    start = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    end = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    if end < start:
        print('\033[91m' + 'End date is not after start date' + '\033[0m')
        raise ValueError, 'End date is not after start date'
    tickersymbol = 'GE'
    averagingwindow = 'w' #weekly average

    payload = {'s': tickersymbol, 
               'a': start.month, 
               'b': start.day, 
               'c': start.year, 
               'd': end.month, 
               'e': end.day,
               'f': end.year, 
               'g': averagingwindow, 
               'ignore': '.csv'}

    r = requests.get(url, params=payload)
    if r.status_code == 200:
        chunk_size = 1024
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)

        with open(filename, 'r') as fd:
            for row in csv.DictReader(fd):
                print("{date}: {volume}".format(date=row['Date'], volume=row['Volume']))
    else:
        print('\033[91m Failed to GET from API. status_code = {status}, message = {message} \033[0m'.format(status=r.status_code, message=r.message))

    r.close()

def main():
    call_api(sys.argv[1], sys.argv[2], 'ge_average_volume.csv')

if __name__ == '__main__':
    main()
