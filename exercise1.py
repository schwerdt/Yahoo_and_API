import urllib
import sys
import csv

#The base url for yahoo finance to get stock prices is stored as a global
#Update it here if it ever changes
yahoo_url ="http://real-chart.finance.yahoo.com/table.csv?s="

def compute_stock_data():
   #Ask the user for a ticker symbol, starting and ending dates
   ticker_symbol = input('Input your ticker symbol as a string: ')
   print "We also need the date range for stock data you want to look at."
   begin_date = input("Beginning date (YYYY-MM-DD): ")
   end_date = input("Ending date (YYYY-MM-DD): ")
 
   #Check date range (make sure end date is after begin date)
   if convert_date_to_int(begin_date) > convert_date_to_int(end_date):
     print "Your ending date was before your beginning date."
     sys.exit()

   #Try to download the file for this ticker symbol
   data_file = retrieve_stock_data_file(ticker_symbol,begin_date,end_date)
   print("We retrieved the stock data")

   #Read the file into a list of dictionaries
   with open(data_file) as f:
       data_table = [val for val in csv.DictReader(f,delimiter=',')]

   print "   Week    Ave Volume"
   for row in data_table:
     print row['Date'], row['Volume']
   


    






def retrieve_stock_data_file(ticker_symbol,begin_date,end_date):
    #Get the day,month, year for the begin and end date
    begin_date = begin_date.split('-')
    end_date = end_date.split('-')
    #Determine the numerical parameters for the begin and end date
    begin_year = begin_date[0]
    begin_month = int(begin_date[1]) - 1
    begin_day = begin_date[2]

    end_year = end_date[0]
    end_month = int(end_date[1]) - 1
    end_day = end_date[2]

    #The month should be in the form 01 for Feb, 11 for Dec
    if begin_month < 10:
      begin_month = '0' + str(begin_month)
    else:
      begin_month = str(begin_month)

    if end_month < 10:                   
      end_month = '0' + str(end_month)
    else:
      end_month = str(end_month)
   
    stock_url = yahoo_url + ticker_symbol 
    #Add begin date
    stock_url = stock_url + '&a=' + begin_month + '&b=' + begin_day + '&c=' + begin_year
    stock_url = stock_url + '&d=' + end_month + '&e=' + end_day + '&f=' + end_year

    #Averaged weekley (g = w)
    stock_url = stock_url + '&g=w'

    #Get the .csv file
    stock_url = stock_url + '&ignore=.csv'
    stock_filename = ticker_symbol + '.csv'

    print stock_url

    #Try to download it.  Since we don't know if the user gave us a valid 
    urllib.urlretrieve(stock_url,stock_filename)
 
    #We don't know if the user gave us a valid ticker symbol, so we need to
    #make sure the file is not a 'Not Found' page
    with open(stock_filename) as f:
        filedata = f.readlines()

    searchfile = [val.find('Not Found') for val in filedata if val.find('Not Found') != -1]
    if len(searchfile) != 0:
        print "The page was not found.  Your ticker symbol or your date range may not"
        print "be valid."
        sys.exit()
    else:
        return stock_filename
 
    


def convert_date_to_int(date_string):
    date_string = date_string.split('-')
    #The reference date will be January 1, 1900.  Dates before this will be negative.  
    year = int(date_string[0])
    month = int(date_string[1])
    date = int(date_string[2])
 
    num_years = year - 1900

    if num_years >= 0:
       num_leapyears = sum([isLeapYear(this_year) for this_year in range(1900,year)]) #[1900,year)
    else:
       num_leapyears = -1*sum([isLeapYear(this_year) for this_year in range(year,1900)]) #[1900,year)

    year_offset = num_years*365 + num_leapyears
    
    #Month offset
    month_offset = 0
    for mo in range(month-1):
        if (mo+1) == 1 or (mo+1) == 3 or (mo+1) ==5 or (mo+1) == 7 or (mo+1) == 8 or (mo+1) == 10 or (mo+1) ==12:
            month_offset += 31
        elif (mo+1) == 4 or (mo+1) == 6 or (mo+1) == 9 or (mo+1) == 11:
            month_offset += 30
        elif (mo+1) == 2:
            if isLeapYear(year):
                month_offset += 29
            else:
                month_offset += 28
        else:
           print("There is a problem with the month.")
           sys.exit()

    return year_offset + month_offset + date + -1
         

    
#Return a logical: True if the tested year is a leap year; False if it is not.
def isLeapYear(year):
  #The year is a leap year if it can be divided by 4 but not 100.  The exception to this rule 
  #occurs when the number can be divided by 400.  
  if year%400 == 0:
    leapyear = True
  elif year%100 == 0:
    leapyear = False
  elif year%4 == 0:
    leapyear = True
  else:
    leapyear = False

  return leapyear





