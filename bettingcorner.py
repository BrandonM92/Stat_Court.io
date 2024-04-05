from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import nba_player
import injury_report

today = datetime.today().date()
global game_data
global player_stats_list
global player_name
global player
global soup
global season_year_player
global proper_name
global player_check


def scrape_stats():
    """This is used to scrape players last 5 games stats. Very similar to what we've done with player so check that
    class for more information. Only change here is we default to 2024 as the year"""
    global player_stats_list
    global player_name
    global player
    global soup
    global season_year_player
    global proper_name
    YEAR = "2024"
    count = "01"
    choice = "N"
    player_name = " "
    player_name = nba_player.user_input_validation_player()
    player = nba_player.translate_name(player_name)
    if player[2] != "N/A":
        count = "02"
    elif player[2] == "N/A":
        count = "01"
    while choice == 'N':
        count = nba_player.player_name_outdated_html(count, player)
        # URL of the player's page
        prediction_url = f"https://www.basketball-reference.com/players/{player[0]}" \
                         f"/{player[1]}{count}/gamelog/{YEAR}"
        # Send an HTTP request to the URL
        response = requests.get(prediction_url)
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            title = soup.select_one("#meta > div:nth-child(2) > h1 > span").text
        except AttributeError:
            print("\nCannot Find The Requested Player, Please Check Spelling")
            return
        else:
            proper_name = " ".join(title.split()[:2])
            print(f"\nChecking all entries that could potentially match {proper_name}.")
            choice = input(f"\nWere you looking for stats on {proper_name}? Y/N: ")
            if choice == 'N':
                count = int(count) + 1
                count = str(f"0{count}")
            else:
                print(f"Checking for {proper_name} player stats for the {YEAR} season")
                # print(soup.prettify())
    else:
        return soup


def last_10_days(soup,option):
    """This searches and organized the last 10 games of data based off today's date and going as far back as 30 days in
    case of breaks or playoffs, etc. It will then output stats for the player IF they played in those games. """

    global game_data
    # Find all rows (assuming each row represents a game)
    try:
        rows = soup.find_all("tr")
    except AttributeError:
        print("Cannot find the player you are looking for. Please make sure your spelling is correct and you enter"
              "\n 'Y' on the correct player.")
        pass
    else:
        # Initialize a list to store game data
        game_data = []

        # Get the current date
        current_date = datetime.now()
        tomorrow = current_date + timedelta(days=1)

        # Calculate the date range (last 30 days)
        start_date = tomorrow - timedelta(days=30)

        # Iterate through each row
        for row in rows:
            date = row.find("td", {"data-stat": "date_game"})
            points_list = row.find("td", {"data-stat": "pts"})
            three_list = row.find("td", {"data-stat": "fg3"})
            assists_list = row.find("td", {"data-stat": "ast"})
            rebounds_list = row.find("td", {"data-stat": "trb"})
            steal_list = row.find("td", {"data-stat": "stl"})
            block_list = row.find("td", {"data-stat": "blk"})

            if date and points_list:
                game_date_str = date.text.strip()
                game_date = datetime.strptime(game_date_str, "%Y-%m-%d")

                # Check if the game date is within the desired range
                if start_date <= game_date <= tomorrow:
                    points = points_list.text.strip()
                    threes = three_list.text.strip()
                    assists = assists_list.text.strip()
                    rebounds = rebounds_list.text.strip()
                    steals = steal_list.text.strip()
                    blocks = block_list.text.strip()
                    if len(game_data) < 10:
                        game_data.append((game_date_str, points, threes, assists, rebounds, steals, blocks))
                    else:
                        pass
        if len(game_data) <= 0:
            print(
                "\nThis player hasn't played this season. We can only check players who are active and currently "
                "playing "
                " in the nba")
            print("\nWe will move on to player prop bet check......")
        else:
            if option == "2":
                choice = input(f"\nAre you looking for the {player_name} last 10 games? (Y/N) \n*DISCLAIMER:\n"
                               "this focuses on the team's last 10 games so any missed games by the \n"
                               "player will be reflected:  ").upper()
                if choice == "Y":
                    # Print the most recent games and their stats
                    print(f"Accessing most Recent Games for : {player_name}:")
                    for game_date, points, threes, assists, rebounds, steals, blocks in game_data:
                        print(f"Date: {game_date}, Points: {points} pts, 3pt Made: {threes}, Assists: {assists} ast, "
                              f"Rebounds: {rebounds} reb, "
                              f"Steals:{steals} , Blocks:{blocks} ")
                    input("\nPress any key to access injury report section")
                    injury_report.get_injury_report(proper_name)
                    input("\nPress any key to move on...")
                    return game_data
                else:
                    return game_data
            else:
                return game_data


def check_user_probability_choice():
    """This is where the user gets to choose his probability percentage that we represent as integers and will handle
    in another method"""
    choice = input(f"\nDo you want to see {player_name}'s stats within the last 10 games, "
                   f"stats hit in \n100% of the Last 10 Games (A), \n80% in Last 10 Games (B),"
                   "\nat least 60% of Last 10 Games(C) or \n40% in Last 10 Games(D)\n"
                   "or (E) to move on to player prop checks.").upper()
    while choice == "A" or choice == "B" or choice == "C" or choice == "D":
        if choice == "A":
            probability = 10
            print(
                f"Searching for any stats achieved at least 100% of games from the last 10"
                f" games or \ngames "
                f"played within the last 10 team games.")
            return probability

        elif choice == "B":
            print(
                f"Searching for any stats achieved at least 80% of games from the last 10 games or \ngames "
                f"played within the last 10 team games.")
            probability = 8
            return probability

        elif choice == "C":
            print(
                f"Searching for any stats achieved at least 60% of games from the last 10 games or \ngames "
                f"played within the last 10 team games.")
            probability = 6

            return probability

        elif choice == "D":
            print(
                f"Searching for any stats achieved at least 40% of games from the last 10 games or \ngames "
                f"played within the last 10 team games.")
            probability = 4
            return probability


def last_ten_day_prop_check(soup):

    """This is where you can check for a player's last 10 games and request an output based on probability"""
    # last_10_soup = scrape_stats()
    game_data_last_10 = last_10_days(soup,option="1")
    # player_check = True
    # Initialize an empty dictionary for the final result
    stats_dict = {
        'Points': [],
        'Threes': [],
        'Assists': [],
        'Rebounds': [],
        'Steals': [],
        'Blocks': []
    }
    # Iterate through the game data
    try:
        for date, points, threes, assists, rebounds, steals, blocks in game_data_last_10:
            stats_dict['Points'].append(points)
            stats_dict['Threes'].append(threes)
            stats_dict['Assists'].append(assists)
            stats_dict['Rebounds'].append(rebounds)
            stats_dict['Steals'].append(steals)
            stats_dict['Blocks'].append(blocks)
    except TypeError:
        print("\nSorry could not access any stats for this player. Potential Reasons: Retired Player or Hasn't Played "
              "in "
              "last 30 days this season")
    else:

        points_list = [stats_dict["Points"]][0]
        three_list = [stats_dict["Threes"]][0]
        assists_list = [stats_dict["Assists"]][0]
        rebounds_list = [stats_dict["Rebounds"]][0]
        steal_list = [stats_dict["Steals"]][0]
        block_list = [stats_dict["Blocks"]][0]
        # print(points_list)
        # print(steal_list)
        # print(block_list)
        if len(points_list) == 0:
            player_confirmation = False
            return player_confirmation

        else:
            choice = "Y"
            while choice == "Y":
                probability = check_user_probability_choice()
                last_ten_display_probability_prop(stat_list=points_list, verb="Scored",
                                                  stat_name="pts",
                                                  probability=probability)
                last_ten_display_probability_prop(stat_list=three_list, verb="Scored",
                                                  stat_name="3pt",
                                                  probability=probability)
                last_ten_display_probability_prop(stat_list=assists_list, verb="gotten",
                                                  stat_name="ast",
                                                  probability=probability)
                last_ten_display_probability_prop(stat_list=rebounds_list, verb="gotten",
                                                  stat_name="rb",
                                                  probability=probability)
                last_ten_display_probability_prop(stat_list=steal_list, verb="gotten",
                                                  stat_name="stl",
                                                  probability=probability)
                last_ten_display_probability_prop(stat_list=block_list, verb="gotten",
                                                  stat_name="blk",
                                                  probability=probability)
                choice = input(f"\nDo you want to see {player_name}'s stats within the last 10 games under different"
                               f" percentages? (Y/N)")
            else:
                pass


def last_ten_display_probability_prop(stat_list, verb, stat_name, probability):
    """last_ten_day_prop_check calls method to get the results outputted if any stats happened as many games as the
    probability count calls for. Example: 10 games - User chooses 80% then it will check if there are any stats that
    happened at least 8 out of those 10 games and print it out. """
    numbers = [int(num) for num in stat_list]
    number_list = []
    count = int(len(numbers))
    # Create a for loop to count from 0 to the upper limit
    for x in range(count):
        for i in range(numbers[x] + 1):
            number_list.append(i)
    # Print the list of numbers
    # print(number_list)
    number_dict = {}
    # Iterate through the given list
    for num in number_list:
        if num in number_dict:
            # Increment the count if the number is already in the dictionary
            number_dict[num] += 1
        else:
            # Initialize the count if the number is encountered for the first time
            number_dict[num] = 1
    # Print the resulting dictionary
    # print(number_dict)
    try:
        percent = max(k for k, v in number_dict.items() if v >= probability)
    except ValueError:

        try:
            updated_prob = round((probability / 10) * count)
            # IF games are less than 10, then we change the probability to match the count.
            percent = max(k for k, v in number_dict.items() if v >= (round((probability / 10) * count)))
            if percent > 0:
                # print("return 1")
                # print(updated_prob)
                return print(f"This player as {verb} at least: {percent} {stat_name} in {updated_prob} of their "
                             f"last {count} games : ({updated_prob}/{count})")
            else:
                return
        except ValueError:
            print("Cannot find player's stats for this season")
            return

    else:
        if percent > 0:
            updated_prob = round((probability / 10) * count)
            # print("return 2")  # IF YOU PLAY 10 GAMES YOU GET HERE
            return print(f"This player as {verb} at least: {percent} {stat_name} in {updated_prob} of their "
                         f"last {count} games : ({updated_prob}/{count})")
        else:
            return


def display_frequency(assists, points, rebounds, threes, steals, blocks):
    """This is where we output the risk frequency"""
    print(f"Points: {points}, {web_scrape_stat_frequency(code='pts', user_number=points)}")
    print(f"Three Points: {threes}, {web_scrape_stat_frequency(code='fg3', user_number=threes)}")
    print(f"Assists: {assists}, {web_scrape_stat_frequency(code='ast', user_number=assists)}")
    print(f"Rebounds: {rebounds}, {web_scrape_stat_frequency(code='trb', user_number=rebounds)}")
    print(f"Steals: {steals}, {web_scrape_stat_frequency(code='stl', user_number=steals)}")
    print(f"Blocks: {blocks}, {web_scrape_stat_frequency(code='blk', user_number=blocks)}")


def web_scrape_stat_frequency(code, user_number):
    """This method is used to get a number from the predictions and scan the webpage to get a count for each
    stat every time the player has accomplished that number or higher to showcase frequency"""
    fg_elements = soup.find_all('td', {f'data-stat': {code}})
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


def check_stat(code):
    fg_elements = soup.find_all('td', {f'data-stat': {code}})
    numbers = [element.text.strip() for element in fg_elements]
    print(numbers)


def bet_check(bet_check_player_name):
    print("\nWelcome to The Betting Corner - *Player Prop Bet Check*")
    if bet_check_player_name == "":
        scrape_stats()
        print(f"\nEnter a player prop from any sports betting site i.e Draftkings, Fanduel"
              f"\nAnd we will let you know how many games this season, {bet_check_player_name}, has reached that stat"
              f"\nor scored/gotten higher. This is simply to show potential and consistency. As always:"
              f"\n\t\t\t\t BET RESPONSIBLY! ")
        choice = input("Enter (Y) to begin, or any other character to go to main menu: ")
        while choice == "Y":
            points = get_float_input("\nEnter a points prop: ")
            threes = get_float_input("\nEnter a three-point prop: ")
            assists = get_float_input("\nEnter an assists amount: ")
            rebounds = get_float_input("\nEnter a rebounds amount: ")
            steals = get_float_input("\nEnter a steals amount: ")
            blocks = get_float_input("\nEnter a block amount: ")

            # points = float(input("\nEnter a points prop? "))
            # threes = float(input("\nEnter a three point prop?"))
            # assists = float(input("\nEnter a assists amount? "))
            # rebounds = float(input("\nEnter a rebounds amount?"))
            # steals = float(input("\nEnter a steals amount? "))
            # blocks = float(input("\nEnter a block amount?"))

            display_frequency(assists=assists, points=points, threes=threes, rebounds=rebounds,
                              steals=steals, blocks=blocks)
            choice = input("\nDo you want to check any other prop bets for this player? Enter (Y) to continue"
                           "\n or any other character to go to main menu: ")
        else:
            print("\nReturning to main menu.")
            return

    else:
        print(f"\nEnter a player prop from any sports betting site i.e Draftkings, Fanduel"
              f"\nAnd we will let you know how many games this season, {bet_check_player_name}, has reached that stat"
              f"\nor scored/gotten higher. This is simply to show potential and consistency. As always:"
              f"\n\t\t\t\t BET RESPONSIBLY! ")
        choice = input("Enter (Y) to begin, or any other character to go to main menu: ")
        while choice == "Y":
            points = get_float_input("\nEnter a points prop: ")
            threes = get_float_input("\nEnter a three-point prop: ")
            assists = get_float_input("\nEnter an assists amount: ")
            rebounds = get_float_input("\nEnter a rebounds amount: ")
            steals = get_float_input("\nEnter a steals amount: ")
            blocks = get_float_input("\nEnter a block amount: ")

            display_frequency(assists=assists, points=points, threes=threes, rebounds=rebounds,
                              steals=steals, blocks=blocks)
            choice = input("Do you want to check any other prop bets for this player? Enter (Y) to continue"
                           "\n or any other character to go to main menu: ")
        else:
            print("Returning to main menu.")
            return


def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid numeric value.")
