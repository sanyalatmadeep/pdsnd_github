import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please choose the city you want to see data for. Choices: [chicago, new york city, washington, all]? ').lower()
    cities = ['chicago', 'new york city', 'washington', 'all']
    while city not in cities:
        city = input('You have not selected a valid option, please select a valid option from [chicago, new york city, washington, all]: ').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Please choose the month you want to see data for. Choices: [january, february, march, april, may, june, all]? ').lower()
    
    while month not in MONTHS:
        month = input('You have not selected a valid option, please select a valid option from [january, february, march, april, may, june, all]: ').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please choose the day of the week you want to see data for. Choices: [monday, tuesday, wednesday, thursday, friday, saturday, sunday, all]? ').lower()
    
    while day not in DAYS:
        day = input('You have not selected a valid option, please select a valid option from  [monday, tuesday, wednesday, thursday, friday, saturday, sunday, all]: ').lower()



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
    if city == 'all':
        df_c = pd.read_csv(CITY_DATA['chicago'])
        df_w = pd.read_csv(CITY_DATA['washington'])
        df_ny = pd.read_csv(CITY_DATA['new york city'])
        df= pd.concat([df_c, df_w, df_ny], ignore_index = True, sort = False)
    else:
        df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    df['hour'] = df['Start Time'].dt.hour
    
    return df

def showData(df):
    """Displays 5 rows at a time of a dataframe"""
    
    print('Displaying first 5 rows of the data ...', '\n', '\n')
    print(df.iloc[0:5,:])
    i = 5
    while True:
        cont = input('Would you like to see more rows from the data? Enter Yes or No \n')
        if cont.lower() != 'yes':
            break
        print(df.iloc[i:i+5,:])
        i = i + 5
            
        
        
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    pop_start_month = df['month'].mode()[0]
    print('Most Popular Start month:', MONTHS[pop_start_month - 1].title())

    # TO DO: display the most common day of week
    print('Most Common day of the week to travel:', df['day_of_week'].mode()[0])

    # TO DO: display the most common start hour
    print('Most Popular Start Hour:', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most Popular Start Station:', df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('Most Popular End Station:', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'].str.cat(df['End Station'], sep = ' - ')
    print('Most Popular Trip from Start Station to End Station:', df['Trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time in seconds:', df['Trip Duration'].sum() / 3600)

    # TO DO: display mean travel time
    print('Average travel time per trip in hours:', df['Trip Duration'].mean() / 3600)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Types of users:\n', '\n', df['User Type'].value_counts().to_string(), '\n')

    # TO DO: Display counts of gender
    try:
        print('Gender Distribution:','\n', df['Gender'].value_counts().to_string(), '\n')
    except KeyError:
        print('Gender data not available for this city \n')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print('Earliest year of birth: ', df['Birth Year'].min())
        print('Most recent year of birth: ', df['Birth Year'].max())
        print('Most common year of birth: ', df['Birth Year'].mode()[0])
    except KeyError:
        print('Birth year information not available for this city \n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        showData(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
