import time
import pandas as pd


# Changing display and console setting to match output
pd.set_option('precision', 2)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_colwidth', 130)

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['january', 'february', 'march', 'april', 'may', 'june']

# Program greeting
print("Hello! Time to explore some US Bike share Data!\n")
print("\nLet's get started....\n")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    # Declaring month and day_of_week as global variables,
    # for filtering in time_stats()
    global month, day_of_week

    # Getting user input for city name
    city = ''
    while city not in CITY_DATA.keys():
        city = input("\nPlease select the name of the city whose data you'd like to analyse:"
                     "\n------------Washington, New York, Chicago-----------\n"
                     "\n       (Enter 'quit' to terminate the program)\n").lower()
        if city == 'quit':
            exit()
        elif city not in CITY_DATA.keys():
            print("\nInvalid input!!. Please try again.\n")

    # Getting user input for month
    month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = ''
    while month not in month_list:
        month = input("\nPlease select the desired month: "
                      "\n-------(January, February, March, April, May, June)-------"
                      "\n          (Enter 'all' for data on all months)\n").lower()
        if month not in month_list:
            print("Invalid input!!. Please try again.\n")

    # Getting user input for day of the week.
    day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day_of_week = ''
    while day_of_week not in day_list:
        day_of_week = input("Please enter the desired day of the week:\n"
                            "-----(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)-----\n"
                            "              (Enter 'all' for data on the whole week)\n").lower()
        if day_of_week not in day_list:
            print("Invalid input!!! Please try again:\n")

    print('-'*50)
    return city, month, day_of_week


def load_data(city, month, day_of_week):
    """
    Loads data for the specified city and filters by month and day if applicable.

    """
    start_time = time.time()

    # Load data file into a data frame
    dframe = pd.read_csv(CITY_DATA[city])

    # Renaming columns to avoid syntax errors
    dframe = dframe.rename(columns={'Unnamed: 0': 'ID', 'Start Time': 'Start_Time',
                                    'End Time': 'End_Time', 'Trip Duration': 'Trip_Duration',
                                    'Start Station': 'Start_Station', 'End Station': 'End_Station',
                                    'User Type': 'User_Type', 'Birth Year': 'Birth_Year'})

    # Dropping ID column since it doesn't figure anywhere in our analysis.
    dframe = dframe.drop(['ID'], axis=1)

    # Convert the Start Time column to datetime
    dframe['Start_Time'] = pd.to_datetime(dframe['Start_Time'])

    # Extract month and day of week from Start Time to create new columns
    dframe['Month'] = dframe['Start_Time'].dt.month
    dframe['Day'] = dframe['Start_Time'].dt.weekday_name

    # Filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new data frame
        dframe = dframe[dframe['Month'] == month]

    # Filter by day of week if applicable
    if day_of_week != 'all':
        # Filter by day of week to create the new data frame
        dframe = dframe[dframe['Day'] == day_of_week.title()]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*50)
    return dframe


def show_summary(dframe):
    """ Displays data frame's first five and last five rows plus basic statistical information."""

    print("\nLoading the first 5 rows of the data frame....\n")
    print(dframe.head())
    print("\nLoading the last five rows of the data frame: \n")
    print(dframe.tail())

    # Displaying sum of null values
    print("\nFinding the sum of null values in the data frame....\n")
    print(dframe.isnull().sum())

    # Basic Statistical analysis of data frame
    print("\nSummary statistics of the data frame: \n")
    print(dframe.describe())


def time_stats(dframe):
    """Displays statistics on the most frequent times of travel."""
    start_time = time.time()
    print('\nCalculating The Most Frequent Times of Travel...\n')

    # Display the most common month
    if month == 'all':
        common_month = int(dframe['Month'].mode())
        common_month_name = months[common_month -1]
        print("The most common month for bike share travel is: {}.".format(common_month_name.title()))

    # Display the most common day of week
    if day_of_week == 'all':
        day_index = dframe['Day'].mode()[0]
        print("\nThe most common day for bike share travel is: {}".format(day_index))

    # Display the most common start hour
    common_hour = dframe['Start_Time'].dt.hour.mode()[0]
    if common_hour == 0:
        time_of_day = 'am'
        readable = 12
    elif 1 <= common_hour < 13:
        time_of_day = 'am'
        readable = common_hour
    elif 13 <= common_hour < 24:
        time_of_day = 'pm'
        readable = common_hour - 12
    print("\nThe most common starting hour is: {}{}".format(readable, time_of_day))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def station_stats(dframe):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_st = dframe['Start_Station'].mode().to_string(index=False)
    print("\nThe most popular start station is:  {}.".format(common_start_st))

    # Display most commonly used end station
    common_end_st = dframe['End_Station'].mode().to_string(index=False)
    print("\nThe most popular end station is:  {}.".format(common_end_st))

    # Display most common or popular trip
    # Creating a column called 'Trip' which concatenates 'Start Station' & 'End Station'
    dframe['Trip'] = dframe['Start_Station'].str.cat(dframe['End_Station'], sep=' -to- ')
    common_trip = dframe['Trip'].mode().to_string(index=False)
    print("\nThe most frequently occurring combination of start and end stations is:\n{}".format(common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def trip_duration_stats(dframe):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_duration = dframe['Trip_Duration'].sum()
    min1, sec1 = divmod(total_duration, 60)
    hr1, min1 = divmod(min1, 60)
    total_days, hr1 = divmod(hr1, 24)
    print("\nThe total trip duration is:  {} days, {} hours, {} minutes and {}"
          " seconds.".format(total_days, hr1, min1, sec1))

    # Display mean travel time
    mean_duration = round(dframe['Trip_Duration'].mean())
    min2, sec2 = divmod(mean_duration, 60)
    hr2, min2 = divmod(min2, 60)
    print("\nThe average / mean travel time is: {} hours, {} minutes and {}"
          " seconds.".format(hr2, min2, sec2))

    # Display the longest trip
    longest_trip = dframe['Trip_Duration'].max()
    min3, sec3 = divmod(longest_trip, 60)
    hr3, min3 = divmod(min3, 60)
    longest_day, hr3 = divmod(hr3, 24)
    print("\nThe longest trip is: {} days, {} hours, {} minutes and {} "
          "seconds.".format(longest_day, hr3, min3, sec3))

    # Display the shortest trip
    shortest_trip = dframe['Trip_Duration'].min()
    min4, sec4 = divmod(shortest_trip, 60)
    hr4, min4 = divmod(min4, 60)
    print("\nThe shortest trip is: {} hours, {} minutes and {} "
          "seconds.".format(hr4, min4, sec4))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def user_stats(dframe):
    """Displays statistics on bike share users. """

    print("\nCalculating User Type Stats...\n")
    start_time = time.time()

    # Display counts of user types
    subscriber = dframe.query('User_Type == "Subscriber"').User_Type.count()
    customer = dframe.query('User_Type == "Customer"').User_Type.count()
    print("\nThere are {} Subscribers and {} Customers.".format(subscriber, customer))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def age_and_gender_stats(dframe):
    """Displays statistics on gender types and birth years"""
    print("\nCalculating Gender and Age Stats....\n")
    start_time = time.time()

    # Display gender counts
    male = dframe.query('Gender == "Male"').Gender.count()
    female = dframe.query('Gender == "Female"').Gender.count()
    print("\nThere are {} Males and {} Females.".format(male, female))

    # Display earliest, most recent, and most common years of birth
    earliest_year = int(dframe['Birth_Year'].min())
    latest_year = int(dframe['Birth_Year'].max())
    common_year = int(dframe['Birth_Year'].mode()[0])
    print("\nThe earliest birth year on record is: {}, while the latest "
          "birth year is: {}".format(earliest_year, latest_year))
    print("\nThe most common year of birth is: {}".format(common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 50)


def display_data(dframe):
    """
    Displays 5 lines of data after prompting the users for input. Following this, asks the users
    whether they would like to view 5 more lines or not.
    """
    response_choice = ['yes', 'no']
    start = 0
    stop = 5

    # Setting a flag in case the user wishes to view more lines of data.
    proceed = True

    user_input = ''
    while user_input not in response_choice:
        user_input = input("\nWould you like to view raw trip data? Enter 'yes' or 'no'.\n").lower()

        if user_input == 'yes' or user_input.startswith('y'):
            print(dframe[dframe.columns[0:-1]].iloc[start:stop])
    while proceed:
        show_more = ''
        while show_more not in response_choice:
            show_more = input("\nWould you like to view 5 more lines of raw trip data? Enter 'yes' or 'no'.\n")
            if show_more.lower() == 'yes' or show_more.startswith('y'):
                start += 5
                stop += 5
                print(dframe[dframe.columns[0:-1]].iloc[start:stop])
            elif show_more.lower() == 'no' or show_more.startswith('n'):
                proceed = False


def main():
    while True:
        city, month, day = get_filters()
        dframe = load_data(city, month, day)

        show_summary(dframe)
        time_stats(dframe)
        station_stats(dframe)
        trip_duration_stats(dframe)
        user_stats(dframe)
        if set(['Gender', 'Birth_Year']).issubset(dframe.columns):
            age_and_gender_stats(dframe)
        display_data(dframe)

        restart = input("\nWould you like to restart the program? Enter 'yes' or 'no'.\n")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
