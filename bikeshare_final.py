import time
import pandas as pd
# er zit een fout in df dag benadering
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#Done
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please type your prefered city; chicago, new york city or washington\n").strip().lower()
        if city not in ['chicago','new york city','washington']:
            print("Please only select from the given cities. Try again...")
            continue
        else:
            break


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please type your prefered month; jan, feb, mar, apr, may, jun or all\n").strip().lower()
        if month not in ['jan','feb','mar','apr','may','jun','all']:
            print("Please only select from the given months. Try again...")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please type your prefered day of the week; mon, tue, wed, thu, fri, sat, sun or all\n").strip().lower()
        if day not in ['mon','tue','wed','thu','fri','sat','sun','all']:
            print("Please only select from the given days. Try again...")
            continue
        else:
            break

    print('-'*40)
    return city, month, day
#Done
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
    df['day'] = df['Start Time'].dt.dayofweek


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the months list to get the corresponding int
        days = ['mon','tue','wed','thu','fri','sat','sun']
        day = days.index(day)

        # filter by day of week to create the new dataframe
        df = df[df['day'] == day]

    return df
#Done
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    #First calc. most traveled month than lookup index to our premade list -1
    most_traveled_month = df['month'].value_counts().idxmax()
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print(months[most_traveled_month-1],'is the most common month!')

    # display the most common day of week
    most_traveled_day = df['day'].value_counts().idxmax()
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    print(days[most_traveled_day],'is the most common week day!')

    # display the most common start hour
    # for this we need to make a new columns
    df['hour'] = df['Start Time'].dt.hour
    print(df['hour'].value_counts().idxmax(),'is the most common start hour!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#Done
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print(start_station,'is the most common starting point!')

    # display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print(end_station,'is the most common end point!')

    # display most frequent combination of start station and end station trip
    # Groupby than compute group sizes than return first row
    most_traveld_route = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('The most traveled route is:\n',most_traveld_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#Done
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time_sec = df['Trip Duration'].sum()
    print(int((travel_time_sec / 3600)),'is the total travel time in hours')
    print(int((travel_time_sec / 60)),'is the total travel time in minutes')

    # display mean travel time
    print(int(df['Trip Duration'].mean()),'is the mean travel time')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#Done
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    # Display counts of gender
    # Not all file have gender, make exception
    gender_in_dataframe = "Gender" in df
    if gender_in_dataframe is False:
        print("Genders are not specified")
    else:
        print(df['Gender'].value_counts(),'is the most commom gender!')

    # Display earliest, most recent, and most common year of birth
    #same issue as gender
    birth_year_in_dataframe = "Birth Year" in df
    if birth_year_in_dataframe is False:
        print("Birth years are not specified")
    else:
        print(int(df['Birth Year'].min()),'is the earliest birth year')
        print(int(df['Birth Year'].max()),'is the most recent brith year')
        print(int(df['Birth Year'].value_counts().idxmax()),'is the most commen birth year')

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

        #For the extra rubric requirement

        raw_data = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n')
        if raw_data.lower() == 'yes':
            start_loc = 0
            while True:
              print(df.iloc[start_loc:start_loc + 5])
              start_loc += 5
              raw_data = input("Do you wish to see 5 more?: yes or no\n ").lower()
              if raw_data.lower() != 'yes' :
                  break
        else:
            print('No raw data is shown')


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
