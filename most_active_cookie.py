import sys
import csv

#TO MAP MONTHS AND NUMBER OF THE DAYS IN THE MONTH
months_days_mapping = {}
months_days_mapping['01'] = '31'
months_days_mapping['02'] = '28'
months_days_mapping['03'] = '31'
months_days_mapping['04'] = '30'
months_days_mapping['05'] = '31'
months_days_mapping['06'] = '30'
months_days_mapping['07'] = '31'
months_days_mapping['08'] = '31'
months_days_mapping['09'] = '30'
months_days_mapping['10'] = '31'
months_days_mapping['11'] = '30'
months_days_mapping['12'] = '31'

#TO CHECK IF THE YEAR IS LEAP YEAR OR NOT
def is_leap_year(year):
    if year % 4 == 0:
        return True
    else:
        return False

#TO PROCESS DATES SUCH THAT IF FOR SOME DATE, THE DATE IS CHANGED DUE TO TIME ZONE. RETURNS THE NEW DATE
def process_time_zone(cookie_date, cookie_time,cookie_time_zone, forward):

    hours = cookie_time.split(':')[0]
    minutes = cookie_time.split(':')[1]
    time_zone_hours = cookie_time_zone.split(':')[0]
    time_zone_minutes = cookie_time_zone.split(':')[1]

    total_hours = int(hours) + (forward) * int(time_zone_hours)
    total_minutes = int(minutes) + (forward) * int(time_zone_minutes)

    if total_minutes >= 60:
        total_hours += 1
        total_minutes = total_minutes % 60

    if total_minutes < 0:
        total_hours -= 1
        total_minutes = -total_minutes % 60

    year = cookie_date.split('-')[0]
    month = cookie_date.split('-')[1]
    date = cookie_date.split('-')[2]

    #IF TIME ZONE CHANGES THE DATE TO NEXT DAY'S DATE
    if total_hours >= 24:

        #CHECK IF YEAR IS LEAP YEAR AND MONTH IS FEB AND PROCESS ACCORDINGLY
        if is_leap_year(int(year)) and month == '02' and date == '29':
            month = '03'
            date = '01'
        elif not is_leap_year(int(year)) and month == '02' and date == '28':
            month = '03'
            date = '01'
        #CHECK IF CURRENT DATE IS LAST DATE OF THE YEAR, IF TRUE WE NEED TO CHANGE THE YEAR TOO
        elif month == '12' and date == '31' in cookie_date:
            month = '01'
            date = '01'
            year = str(int(year)+1)
        #CHECK IF END OF THE MONTH FOR MONTH HAVING 31 DAYS
        elif date == '31' in cookie_date:
            month = str(int(month) + 1)
            if len(month) == 1:
                month = '0' + month
            date = '01'
        # CHECK IF END OF THE MONTH FOR MONTH HAVING 30 DAYS
        elif date == '30' in cookie_date and months_days_mapping[month] == '30':
            month = str(int(month) + 1)
            if len(month) == 1:
                month = '0' + month
            date = '01'
        #IF NONE OF THE ABOVE IS SATISFIED JUST CHANGE THE DATE TO NEXT DAY'S DATE
        else:
            date = str(int(date) + 1)
            if len(date) == 1:
                date = '0' + date
    #IF TIME ZONE CHANGES THE DATE TO PREVIOUS DAY'S DATE
    if total_hours < 0:
        # CHECK IF YEAR IS LEAP YEAR AND MONTH IS FEB AND PROCESS ACCORDINGLY
        if is_leap_year(int(year)) and month == '03' and date == '01':
            month = '02'
            date = '29'
        elif not is_leap_year(int(year)) and month == '03' and date == '01':
            month = '02'
            date = '28'
        #CHECK IF FIRST DATE OF THE YEAR, WE WILL NEED TO CHANGE YEAR TO PREVIOUS YEAR AND LAST DATE OF THAT YEAR
        elif month == '01' and date == '01':
            year = str(int(year) - 1)
            date = '31'
            month = '12'
        #CHECK IF FIRST DATE OF A MONTH
        elif date == '01':
            new_month = str(int(month) - 1)

            if len(new_month) == 1:
                new_month = '0' + new_month

            if months_days_mapping[new_month] == '31':
                date = '31'
                month = new_month
            else:
                date = '30'
                month = new_month
        #ELSE JUST CHANGE DATE TO PREVIOUS DAY'S DATE
        else:
            date = str(int(date) - 1)
            if len(date) == 1:
                date = '0' + date

    return year + '-' + month + '-' + date

#RETURNS LIST OF MOST ACTIVE COOKIE
def most_active_cookie(file,date):

    cookie_count_mapping = {}

    try:

        with open(file, newline='') as csvfile:

            csvreader = csv.reader(csvfile)

            for row in csvreader:

                forward = 0
                cookie_name = row[0]
                cookie_date = (row[1].split('T'))[0]

                if '+' in row[1]:
                    cookie_time = (row[1].split('T'))[1].split('+')[0]
                    forward = 1
                    cookie_time_zone = row[1].split('+')[1]
                else:
                    cookie_time = (row[1].split('T'))[1].split('-')[0]
                    forward = -1
                    cookie_time_zone = (row[1].split('T')[1]).split('-')[1]

                cookie_date = process_time_zone(cookie_date, cookie_time,cookie_time_zone, forward)

                if cookie_date == date:
                    if cookie_name in cookie_count_mapping:
                        temp = cookie_count_mapping.get(cookie_name)
                        cookie_count_mapping[cookie_name] = temp + 1
                    else:
                        cookie_count_mapping[cookie_name] = 1

    except FileNotFoundError:
        print("File not found")
        return


    max = 0
    most_active_cookies = []

    for cookie, count in cookie_count_mapping.items():
        if max < count:
            max = count

    for cookie, count in cookie_count_mapping.items():
        if count == max:
            most_active_cookies.append(cookie)

    return most_active_cookies

#EXTRACT THE ARGUMENTS FROM COMMAND LINE AND VALIDATE THEM
def extract_arguments():

    if len(sys.argv)>=3:
        if '.csv' in sys.argv[1] and len(sys.argv[3]) == 10 and sys.argv[3][0:4].isdigit() and sys.argv[3][4] == '-' and sys.argv[3][5:7].isdigit() and sys.argv[3][7] == '-' and sys.argv[3][8:10].isdigit():
            return sys.argv[1], sys.argv[3]

    return None,None

if __name__ == "__main__":

    file,date = extract_arguments()

    if file is not None:
        most_active_cookies = most_active_cookie(file,date)
        for cookie in most_active_cookies:
            print(cookie)
    else:
        print("Problem in command line arguments")