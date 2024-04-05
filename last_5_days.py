import requests
from bs4 import BeautifulSoup
import nba_player

global player_stats_list
global season_year_player
global name


def scrape_stats():
    global predict_soup
    """This is used to scrape players last 5 games stats. Very similar to what we've done with player so check that
class for more information. Only change here is we default to 2024 as the year"""
    YEAR = "2024"
    count = "01"
    choice = "N"
    print("\nEntering: Last 5/Stat Prediction Section")
    player_name = nba_player.user_input_validation_player()
    player = nba_player.translate_name(player_name)
    if player[2] != "N/A":
        count = "02"
    elif player[2] == "N/A":
        count = "01"
    while choice == 'N':
        count = nba_player.player_name_outdated_html(count,player)
        # URL of the player's page
        url = f"https://www.basketball-reference.com/players/{player[0]}/{player[1]}{count}.html"
        prediction_url = f"https://www.basketball-reference.com/players/{player[0]}/{player[1]}{count}" \
                         f"/gamelog/{YEAR}"

        # Send an HTTP request to the URL
        response = requests.get(url)
        response2 = requests.get(prediction_url)
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        predict_soup = BeautifulSoup(response2.content, 'html.parser')
        try:
            title = soup.select_one("#meta > div:nth-child(2) > h1 > span").text
        except AttributeError:
            print("Could not find player. Please Check Spelling or Enter Y On the correct player.")
            return
        else:
            name = " ".join(title.split()[:2])
            print(f"\nChecking all entries that could potentially match {name}.")
            choice = input(f"\nWere you looking for stats on {name}? Y/N: ")
            if choice == 'N':
                count = int(count) + 1
                count = str(f"0{count}")
            else:
                print(f"Checking for {name} player stats for the {YEAR} season")
    else:
        return soup, predict_soup


def get_player_stats(soup):
    """Access table from the webpage with the id: last5 and assigns that data to player_stats_list as a dict
    and returns it """
    table = soup.find('table', {'id': 'last5'})
    # Initialize an empty list to store data that was scraped
    data = []
    # Find all rows in the table
    try:

        rows = table.find_all('tr')
    except AttributeError:
        print(f"Cannot find {name} stats for this year ({season_year_player})")
        print("\nPlease Ensure You are entering 'Y' on the right player's name. \nSome players have similar ID's "
              "based on same last name and similar spelling in their first names.")
        pass
    else:
        # For loop for each row
        for row in rows:
            # Find all cells in the row
            cells = row.find_all(['th', 'td'])
            # Extract data and append to list
            data.append([cell.get_text(strip=True) for cell in cells])
        # Separate header and stats
        header = data[0]
        stats_list = data[1:]
        # Create a list of dictionaries for each player's stats
        player_stats_list = []
        for stats in stats_list:
            player_stats_dict = {key: value for key, value in zip(header, stats)}
            player_stats_list.append(player_stats_dict)
        return player_stats_list


def print_player_stats():
    """Prints out the stats it gets from player_stats_list"""
    choice = input("Do you want the last 5 game breakdown then the Average? (Y) or Just the Average? (N)").upper()
    if choice == "Y":
        for player_stats in player_stats_list:
            print(f"Date: {player_stats['Date']}")
            print(f"Team: {player_stats['Team']}")
            print(f"Opponent: {player_stats['Opp']}")
            print(f"MP: {player_stats['MP']} minutes")
            print(f"Points: {player_stats['PTS']}")
            print(f"FG: {player_stats['FG']} / {player_stats['FGA']} : {player_stats['FG%']} %")
            print(f"3P: {player_stats['3P']} / {player_stats['3PA']} : {player_stats['3P%']} %")
            print(f"FT: {player_stats['FT']} / {player_stats['FTA']} : {player_stats['FT%']} %")
            print(f"ORB: {player_stats['ORB']} / DRB: {player_stats['DRB']} = TRB:{player_stats['TRB']}")
            print(f"Assists: {player_stats['AST']}")
            print(f"STL: {player_stats['STL']}")
            print(f"BLK: {player_stats['BLK']}")
            print(f"PF: {player_stats['PF']}")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            input("Enter Any Key to continue.....")
    else:
        return


def stat_predictor():
    """This takes the averages from the last 5 games, and we calculate the next game score by dividing the average
    by 5 and then multiplying it by 0.75. We will be testing out weighted averages shortly"""
    points_avg = 0
    rb_avg = 0
    ast_avg = 0
    threes_made = 0
    weight_avg_counter = 0.1
    for player_stats in player_stats_list:
        points_avg += (float(player_stats['PTS']) * weight_avg_counter)
        rb_avg += (float(player_stats['TRB']) * weight_avg_counter)
        ast_avg += (float(player_stats['AST']) * weight_avg_counter)
        threes_made += (float(player_stats['3P']) * weight_avg_counter)
        weight_avg_counter += 0.05
    output_prediction_stats(ast_avg, points_avg, rb_avg, threes_made)


def web_scrape_stat_frequency(code, user_number):
    """This method is used to get a number from the predictions and scan the webpage to get a count for each
    stat every time the player has accomplished that number or higher to showcase frequency"""
    fg_elements = predict_soup.find_all('td', {f'data-stat': {code}})
    numbers = [element.text.strip() for element in fg_elements]

    # Create a dictionary to count occurrences
    number_counts = {}
    for num in numbers:
        if num in number_counts:
            number_counts[num] += 1
        else:
            number_counts[num] = 1

    """This checks if the number is in the list"""
    int_numbers = [int(num) for num in numbers]

    # Count occurrences of user_number and numbers greater than it
    frequency = sum(1 for num in int_numbers if num >= user_number)
    games_played = len(numbers)

    return f"He has achieved this in: {frequency}/ {games_played} games this season"


def clamp(value, min_value, max_value):
    """This is where I call to prevent getting negative numbers when I am outputting my prediction stats. This was
    courtesy of researching for ways using math-related functionalities"""
    return max(min(value, max_value), min_value)


def output_prediction_stats(ast_avg, points_avg, rb_avg, threes_made):
    """This is where we do the prediction stats output with 3 levels of risk"""
    low_points = clamp(int(points_avg - 6), 0, float('inf'))
    low_rebounds = clamp(int(rb_avg - 2), 0, float('inf'))
    low_assists = clamp(int(ast_avg - 2), 0, float('inf'))
    low_threes = clamp(int(threes_made - 1), 0, float('inf'))

    med_points = clamp(int(points_avg) - 3, 0, float('inf'))
    med_rebounds = clamp(int(rb_avg) - 1, 0, float('inf'))
    med_assists = clamp(int(ast_avg) - 1, 0, float('inf'))
    med_threes = clamp(int(threes_made) - 0, 0, float('inf'))

    high_points = int(points_avg + 3)
    high_rebounds = int(rb_avg + 2)
    high_assists = int(ast_avg + 2)
    high_threes = int(threes_made + 1)
    print("\nWe offer 3 different predictions based off 3 separate levels of risk ranging from low which is more"
          " likely to hit, medium which is around their season average, and high risk "
          "which is possible but less likely")
    print("\nNote: This does not account for injuries, opponents, minute rotation, etc. This is just based off "
          "their last 5 games averages.")
    choice = input("\nPlease choose a risk level: 'L' for Low Risk, 'M' for Medium Risk, 'H' for High Risk "
                   "or 'A' to see all of them at once: ").upper()
    if choice == "L":
        display_risk_frequency(risk="Low", assists=low_assists, points=low_points, rebounds=low_rebounds,
                               threes=low_threes)
    elif choice == "M":
        display_risk_frequency(risk="Medium", assists=med_assists, points=med_points, rebounds=med_rebounds,
                               threes=med_threes)
    elif choice == "H":
        display_risk_frequency(risk="High", assists=high_assists, points=high_points, rebounds=high_rebounds,
                               threes=high_threes)
    elif choice == "A":
        display_risk_frequency(risk="Low", assists=low_assists, points=low_points, rebounds=low_rebounds,
                               threes=low_threes)
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        display_risk_frequency(risk="Medium", assists=med_assists, points=med_points, rebounds=med_rebounds,
                               threes=med_threes)
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        display_risk_frequency(risk="High", assists=high_assists, points=high_points, rebounds=high_rebounds,
                               threes=high_threes)
    else:
        pass


def display_risk_frequency(risk, assists, points, rebounds, threes):
    """This is where we output the risk frequency"""
    print(f"Stat Predictor ({risk} Risk)")
    print(f"Points: {points}, {web_scrape_stat_frequency(code='pts', user_number=points)}")
    print(f"Three Points: {threes}, {web_scrape_stat_frequency(code='fg3', user_number=threes)}")
    print(f"Assists: {assists}, {web_scrape_stat_frequency(code='ast', user_number=assists)}")
    print(f"Rebounds: {rebounds}, {web_scrape_stat_frequency(code='trb', user_number=rebounds)}")
    input("Enter a Key to continue")


def last_5_average():
    """This method handles calculating and printing out last 5 games stats"""
    points_avg = 0
    rb_avg = 0
    ast_avg = 0
    threes_made = 0
    for player_stats in player_stats_list:
        points_avg += int(player_stats['PTS'])
        rb_avg += int(player_stats['TRB'])
        ast_avg += int(player_stats['AST'])
        threes_made += int(player_stats['3P'])
    print("LAST 5 AVERAGES:")
    print(f"Points: {round(points_avg / 5)}")
    print(f"3P: {threes_made / 5}")
    print(f"Assists: {ast_avg / 5}")
    print(f"Rebounds: {rb_avg / 5}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


def choose_option():
    """This is the MAIN LOOP for this class and will give the user prompts to see which function they want to access
"""
    global player_stats_list
    try:
        player_stats_list = get_player_stats(soup=scrape_stats()[0])
    except TypeError:
        print("")
        return
    else:
        if player_stats_list is not None:
            choice = input("Do you want to see the player's last five games of stats?")
            if choice == "Y":
                print_player_stats()
                last_5_average()
                selection = input("Do you want us predict their stats for their next game?")
                if selection == "Y":
                    stat_predictor()
                else:
                    pass

            if choice == "N":
                selection = input("Do you want us predict their stats for their next game?")
                if selection == "Y":
                    stat_predictor()
                else:
                    print("Thank you for using our program")
        else:
            print("Back to main menu.")
