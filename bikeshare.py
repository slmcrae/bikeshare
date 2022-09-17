
""" Sherri McRae
    Python Project
    Programming for Data Science
    Date: 1/9/2022
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }
cities = ['chicago','new york','washington']
months = ['january','february','march','april','may','june']
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def raw_data(df):
    """ Print raw data, 5 lines at a time until either there are no more
    lines left or until the user ends the session.
    arguments: dataframe
    returns 'None'
    prints 5 rows of dataframe at a time.
    """
    start = -5
    end = 0
    # ask user if they would like to see the raw data
    print("\n\nThere are {} rows in this dataset.".format(len(df.index)))
    print("\nWould you like to see the raw data?")
    while True:
        # Get user input to view 5 lines of data
        display_data = input("Enter yes to view the next 5 lines or no to end the session: ").lower()
        # if user enters yes, then determine which rows need to be shown.       
        if display_data == 'yes':
            # if the end of the slice is already more than the number of rows in set
            if (end) > (len(df.index)-1):
                print("\n\nNo further data to display")
                print("Session end\n\n")
                break
            # if the end point of slice is closer than 5 away from end of data
            elif (end + 5) > (len(df.index)-1):
                start += 5
                end += (end + (len(df.index)-1-end))
                section = df.iloc[start:end,]
                print(section)
                print("\n\nNo further data to display.")
                print("Session end\n\n")
                break
            # standard slice of 5 rows of data
            else:
                start += 5
                end += 5
                section = df.iloc[start:end,]
                print(section)                                    
        else:
            print("\n\nRaw data session ended.")
            break
                
        
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('We have data from 3 cities: Washington, Chicago and New York')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:         
        city = input("\nWhich city's data would you like to explore?\nEnter city:  ").lower()
        if city not in cities:
            print("\nThat is not a valid city. Please select one of the following:\n", list(CITY_DATA.keys()))
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nplease enter a month from January to June or enter 'all': ").lower()
        if month == 'all':
            print("You have selected all months")
            break
        elif month not in months:
            print("\nThat was an invalid entry. Please try again.")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nPlease enter a day of the week or 'all':  ").lower()
        if day == 'all':
            print("You have selected all days of the week")
            break
        elif day not in days:
            print("\nThat was not a day of the week.\nPlease check your spelling and re-enter.\n")
        else:
            break
    
    print("\n\nYour selection ~")
    print("City: {}, Month: {}, Day: {}".format(city.title(), month.title(), day.title()))
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
    df = pd.read_csv(CITY_DATA[city.title()])
     
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of the week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
       
    
    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month.title()]
    
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']== day.title()]
         
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if len(list(df['month'].unique())) > 1:
        most_common_month = df['month'].mode()[0]
        print("The most popular month is for bike rides is {}.".format(most_common_month))
      
    # display the most common day of week
    if len(list(df['day_of_week'].unique())) > 1:
        most_common_day = df['day_of_week'].mode()[0]
        print("Thie most common day of the week for bike rides is {}".format(most_common_day))

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print("The most popular time to go on a bike ride is {}:00.".format(most_common_hour))
    
      
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip Route...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print("The most popular start station is {}".format(most_common_start))
      
    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print("The most popular end station is {}.".format(most_common_end))

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    most_common_trip = df['trip'].mode()[0]
    print("The most popular trip route is {}.".format(most_common_trip))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

     # display total travel time
    total_all_trips = df['Trip Duration'].sum()
    hours_in_mil = round(total_all_trips/1000000,3)
   
    print("The total time spent riding bikes was {} million hours.".format(hours_in_mil))
        
    # display mean travel time
    average_trip = df['Trip Duration'].mean()
    average_trip_hours = int(average_trip/60)
    average_trip_mins = int(average_trip%60)
    print("The average length of a bike ride was {} hours and {} minutes.".format(average_trip_hours, 
           average_trip_mins))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nUser Types: ")
    users = df['User Type'].unique()
    i=0
    for i in range(len(users)):
        count = list(df['User Type']).count(users[i])
        print("{}: {}".format(users[i], count)) 
        i += 1
   
    # Display counts of gender
    print("\nGender Breakdown: ")
    i = 0
    try:
        genders = ['Male','Female']
        for gender in genders:
            count = list(df['Gender']).count(gender)
            print("{}: {}".format(gender, count)) 
            i += 1
        unknown = df['Gender'].isnull().sum()
        print("Unknown: {}".format(unknown))
    except:
         print("There is no gender data for this city.")
    
        
    # Display earliest, most recent, and most common year of birth
    print("\nBirth Year Data:")
    try:
        mode_year = int(df['Birth Year'].mode()[0])
        max_year = int(df['Birth Year'].max())
        min_year = int(df['Birth Year'].min())
        print("\nThe most frequent birth year is: {}".format(mode_year))
        print("The most recent birth year is: {}".format(max_year))
        print("The earliest birth year is: {}".format(min_year))
    except:
        print("There is no birth year data for this city.")
    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
