import pytest
import most_active_cookie
import sys
import csv

def test_is_leap_year():
    res = most_active_cookie.is_leap_year(2024)
    assert res == True
    res = most_active_cookie.is_leap_year(2021)
    assert res == False
    res = most_active_cookie.is_leap_year(2000)
    assert res == True

@pytest.mark.parametrize("cookie_date, cookie_time, cookie_time_zone, forward, expected", [
    ('2024-03-17', '19:58:00', '00:00', 1, '2024-03-17'),  # No time zone ( UTC )
    ('2024-03-17', '19:58:00', '05:30', 1, '2024-03-18'),  # Forward time zone
    ('2024-03-17', '02:58:00', '05:30', -1, '2024-03-16'),  # Backward time zone
    ('2023-11-30', '19:58:00', '08:30', 1, '2023-12-01'),  # Forward time zone and month end with 30
    ('2024-01-31', '22:58:00', '03:30', 1, '2024-02-01'),  # Forward time zone and month end with 31
    ('2024-02-29', '23:58:00', '02:30', 1, '2024-03-01'),  # Forward time zone and leap year and Feb
    ('2023-02-28', '22:58:00', '04:30', 1, '2023-03-01'),  # Forward time zone and non leap year and Feb
    ('2024-03-01', '09:58:00', '10:30', -1, '2024-02-29'),  # Backward time zone and leap year and 1st March
    ('2023-03-01', '09:58:00', '10:30', -1, '2023-02-28'),  # Backward time zone and non leap year and 1st March
    ('2024-02-01', '06:58:00', '08:30', -1, '2024-01-31'),  # Backward time zone and month 31 first date
    ('2023-05-01', '03:58:00', '04:30', -1, '2023-04-30'),  # Backward time zone and month 30 first date
    ('2023-12-31', '17:58:00', '10:30', 1, '2024-01-01'),  # Forward time zone and last day of the year
    ('2024-01-01', '03:58:00', '5:30', -1, '2023-12-31'),  # Backward time zone and first day of the year
])
def test_process_time_zone_with_utc_time(cookie_date, cookie_time, cookie_time_zone, forward, expected):
    res = most_active_cookie.process_time_zone(cookie_date,cookie_time,cookie_time_zone,forward)
    assert res == expected


@pytest.mark.parametrize("csv_data, target_date, expected_result", [
    (  # Original Test Case
        [
            ['AtY0laUfhglK3lC7', '2018-12-09T14:19:00+00:00'],
            ['SAZuXPGUrfbcn5UA', '2018-12-09T10:13:00+00:00'],
            ['5UAVanZf6UtGyKVS', '2018-12-09T07:25:00+00:00'],
            ['AtY0laUfhglK3lC7', '2018-12-09T06:19:00+00:00'],
            ['SAZuXPGUrfbcn5UA', '2018-12-08T22:03:00+00:00'],
            ['4sMM2LxV07bPJzwf', '2018-12-08T21:30:00+00:00'],
            ['fbcn5UAVanZf6UtG', '2018-12-08T09:30:00+00:00'],
            ['4sMM2LxV07bPJzwf', '2018-12-07T23:30:00+00:00'],

        ],
        '2018-12-09',
        ['AtY0laUfhglK3lC7']
    ),
    (  # Multiple cookies with same count
            [
                ['cookie1', '2018-12-09T14:19:00+00:00'],
                ['cookie2', '2018-12-09T10:13:00+00:00'],
                ['cookie1', '2018-12-09T07:25:00+00:00'],
                ['cookie2', '2018-12-09T06:19:00+00:00'],
            ],
            '2018-12-09',
            ['cookie1','cookie2']
    ),
    (  # Forward time zone
            [
                ['cookie1', '2018-12-09T14:19:00+10:00'],
                ['cookie2', '2018-12-09T10:13:00+00:00'],
                ['cookie1', '2018-12-09T07:25:00+00:00'],
                ['cookie2', '2018-12-09T06:19:00+00:00'],
            ],
            '2018-12-09',
            ['cookie2']
    ),
    (  # Backward time zone
            [
                ['cookie1', '2018-12-09T14:19:00+00:00'],
                ['cookie2', '2018-12-09T10:13:00+00:00'],
                ['cookie1', '2018-12-09T07:25:00-10:00'],
                ['cookie2', '2018-12-09T06:19:00+00:00'],
            ],
            '2018-12-09',
            ['cookie2']
    ),
])
def test_most_active_cookie(csv_data, target_date, expected_result):

    with open('temp_cookie_data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(csv_data)

    most_active_cookies = most_active_cookie.most_active_cookie('temp_cookie_data.csv', target_date)
    assert most_active_cookies == expected_result

def test_most_active_cookie_with_wrong_file_name():

    try:
        most_active_cookie.most_active_cookie('nonexistent_file.csv', '2022-01-01')
    except FileNotFoundError:
        assert True

@pytest.mark.parametrize("script_name, file_name, flag, target_date, expected_file, expected_date", [
    ('script_name.py', 'input_file.csv', '-d', '2024-03-17', 'input_file.csv','2024-03-17'),
    ('script_name.py', 'input_file', '-d', '2024-03-17', None, None),
    ('script_name.py', 'input_file', '-d', '2024', None, None),
    ('script_name.py', 'input_file', '-d', '202417', None, None),
    ('script_name.py', 'input_file', '-d', 'abcd-ef-gh', None, None),
])
def test_extract_arguments_valid(script_name, file_name, flag, target_date, expected_file, expected_date):
    sys.argv = [script_name, file_name, flag, target_date]  # Set command-line arguments

    arg1, arg2 = most_active_cookie.extract_arguments()

    assert arg1 == expected_file
    assert arg2 == expected_date

    sys.argv = ['python', 'script_name.py'] # Set command-line arguments

    arg1, arg2 = most_active_cookie.extract_arguments()

    assert arg1 == None
    assert arg2 == None

if __name__ == '__main__':
    pytest.main()