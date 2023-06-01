import time
import pandas as pd
import numpy as np
from datetime import datetime as dt
import calendar as c

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    #calculate the appropriate greeting for the user. This is then used to greet the user at the beginning
    current_time = dt.now()
    if current_time.hour < 12:
        greeting ="Good morning!"
    elif current_time.hour >= 12 and current_time.hour < 17:
        greeting ="Good afternoon!"
    else:
        greeting ="Good evening!"

    #start by greeting the user and asking if they want to look at bikeshare data
    while True:
        start_question = input('\n{} Would you like to take a look at some date on bike shares? yes/no\n'.format(greeting)).lower()
        if start_question != 'yes':
            print("\nSorry, that\'s the wrong answer! ;)\n")
            continue
        else:
            break

    # user input for city (chicago, new york city, washington).

    while True:
        city = input("\nChoose a city to filter by: New York, Chicago or Washington?\n").lower()
        cities = ('new york', 'chicago', 'washington')
        if city not in cities:
            print("\nSorry, {} is not an option. Choose a city to filter by: New York, Chicago or Washington?".format(city))
            continue
        else:
            break

    # user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWhich month are you interested in? january, february, march, april, may or june, or type \'all\' if you want all months.\n>').lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        if month not in months:
            print("\nSorry, {} is not an option. Which month are you interested in? january, february, march, april, may or june, or type \'all\' if you want all months.". format(month))
            continue
        else:
            break

    #  user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWhat day of the week are you interested in? Or type \'all\' for all the days of the week.\n>').lower()
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
        if day not in days:
            print("\nSorry, {} is not an option. What day of the week are you interested in? Or type \'all\' for all the days of the week.". format(day))
            continue
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating the most frequent times of travel...\n')
    start_time = time.time()

    # display the most common month unless just one month is selected
    month_count = len(pd.unique(df['month']))
    if month_count == 1:
        print('Select all months to view the most common month of travel')
    else:
        common_month = df['month'].mode()[0]
        month_name = c.month_name[common_month]
        print('The most common month of travel was', month_name)

    # display the most common day of week
    day_count = len(pd.unique(df['day_of_week']))
    if day_count == 1:
        print('Select all days to view the most common day of travel')
    else:
        common_day = df['day_of_week'].mode()[0]
        print('The most common day of the week to travel was', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    if common_hour > 12:
        readable_common_hour = str(common_hour - 12) + 'PM'
    else:
        readable_common_hour = str(common_hour) + 'AM'
    print('The most common hour to travel was', readable_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the most popular stations and trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most common station to start at was', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most common station to end at was', end_station)

    # display most frequent combination of start station and end station trip
    combination_station = ('starting at ' + df['Start Station'] + ' and ending at ' + df['End Station']).mode()[0]
    print('The most common trip was', combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating trip duration...\n')
    start_time = time.time()

    # display total travel time - note that trip duration is recorded in seconds
    total_travel_time = sum(df['Trip Duration'])
    total_days = int(total_travel_time/86400)
    leftover_hours = round((total_travel_time % 86400)/3600)
    print('The total travel time is {} days and {} hours'.format(total_days, leftover_hours))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_hours = int(mean_travel_time/3600)
    leftover_minutes = round((total_travel_time % 3600)/60)
    print('The mean travel time for a bike ride is {} hours and {} minutes'.format(mean_hours,leftover_minutes))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating user stats...')
    start_time = time.time()

    # Display counts of user types
    types_count = df['User Type'].value_counts()
    print('\nUser Types:\n', types_count)


    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nUser Genders:\n', gender_count)
    except KeyError:
        print('\nSorry, we have no gender data for this city.')


    # Display earliest, most recent, and most common year of birth
    # !! Note that the ages are an estimate given we only have access to the year of birth not the date.
    # 2017 is given as the current_year as all data is from 2017, the value of current_year could be changed later if a wider sample size is selected
    current_year = 2017

    try:
        earliest_year = df['Birth Year'].min()
        oldest_user = current_year - earliest_year
        print('\nOldest User:', int(oldest_user))
    except KeyError:
        print("\nSorry, we have no user birth year data for this city.")

    try:
        latest_year = df['Birth Year'].max()
        youngest_user = current_year - latest_year
        print('\nYoungest User:', int(youngest_user))
    except KeyError:
        print("\nSorry, we have no user birth year data for this city.")

    try:
        average_year = df['Birth Year'].mode()[0]
        average_age = current_year - average_year
        print('\nAverage User Age:', int(average_age))
    except KeyError:
        print("\nSorry, we have no user birth year data for this city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Raw data is displayed if the user wants to see it. They can keep viewing the next 5 rows if they want to
    Args:
        df - Relevant data frame given the city, month and day the user has selected
    """
    response = ['yes','no']
    index = 0
    while True:
        raw_data = input("\nDo you want to see 5 rows of raw data? yes/no\n").lower()
        if raw_data == 'yes' and index == 0:
            print(df.head())
            index += 5
            break
        elif raw_data not in response:
            print("Sorry, that\'s not an option, please try again")
        else:
            break


    if raw_data != 'no':
        index = 5
        while True:
            next_raw_data = input("\nDo you want to see the next 5 rows of raw data? yes/no\n").lower()
            if next_raw_data == 'yes':
                print(df[index:index+5])
                index += 5
            elif next_raw_data not in response:
                print("Sorry, that\'s not an option, please try again")
            else:
                break

def main():
    """this is the final output of the code, after completion the user is asked whether they want to end the code or restart"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
