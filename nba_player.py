import requests
from bs4 import BeautifulSoup

team1 = ""
team2 = ""
proper_name = ""


def translate_name(name):
    """This method allows me to take a name input and split it up to return for use with the URL to make soup
    if the player has 3 names (ex. Jaren Jackson Jr) or a hyphen in name, it accounts for it and allows me to
    continue."""
    parts = name.split()

    if len(parts) == 3:
        first_name = parts[0]
        jr = parts[2]
        last_name = parts[1]
        first_initials = first_name[:2].lower()
        last_initials = last_name[:5].lower()
        initial = last_name[0].lower()
        username = f"{last_initials}{first_initials}".lower()
        return initial, username, jr
    else:
        first_name = parts[0]
        last_name = parts[-1]
        first_initials = first_name[:2].lower()
        last_initials = last_name[:5].lower()
        initial = last_name[0].lower()
        username = f"{last_initials}{first_initials}".lower()
        username = fixing_url_player_name(username)
        jr = "N/A"
        return initial, username, jr


def fixing_url_player_name(username):
    """This is to be added to whenever a player name is discovered. Some instances like Clint Capela should be
    capelcl but for some reason basketball references does capelcl. So for other instances like this we will
    fix it here."""
    if username == 'capelcl':
        username = "capelca"
    elif username == "hendrta":
        username = "hendrita"
    return username


def web_scrape(player_year, player):
    """This method allows me to take the name from translate_name, and apply it to the web-scraping URL. From
    there I will process it with beautiful soup and if the player has a similar name id (ex. Antonio Davis &
    Anthony Davis) it will ask the user one by one if this is the player they are looking for. If the first name
    isn't right, then it will increase count by 1 and try again until the player you are looking for is prompted.
    If I want to scale this program, I will uncomment out the soup variable and use it to determine how to access
    new stats """
    global proper_name
    player_soup = ""
    count = ""
    choice = "N"
    if player[2] != "N/A":
        count = "02"
    elif player[2] == "N/A":
        count = "01"
    while choice == 'N':
        count = player_name_outdated_html(count, player)
        print(count)
        URL = f"https://www.basketball-reference.com/players/{player[0]}/{player[1]}{count}.html"
        response = requests.get(url=URL)
        data = response.text
        player_soup = BeautifulSoup(data, "html.parser")
        # print(player_soup.prettify())
        try:
            title = player_soup.select_one("#meta > div:nth-child(2) > h1 > span").text
        except AttributeError:
            print("Cannot Find The Requested Player, Please Check Spelling")
            return
        else:
            proper_name = " ".join(title.split()[:2])
            print(f"\nChecking all entries that could potentially match {proper_name}.")
            choice = input(f"\nWere you looking for stats on {proper_name}? Y/N: ")
            if choice == 'N':
                count = int(count) + 1
                count = str(f"0{count}")
            else:
                print(f"Checking for {proper_name} player stats for the {player_year} season")
    else:
        return player_soup


def player_name_outdated_html(count, player):
    """If I come across bugs for players like in the Tobias Harris case, then I can just fix it right here."""
    print(player)
    if player[1] == "harrito":
        print("Adjusting URL Due to HTML. Grabbing Tobias Harris Data.")
        count = "02"
    elif player[1] == "thomaca":
        print("Adjusting URL Due to HTML. Grabbing Cam Thomas Data")
        count = "02"
    elif player[1] == "willija":
        choice = int(input("Are you looking for (1) Jay Williams, (2) Jawad Williams, (3) Jalen Williams, "
                       "(4) Jaylin Williams?"))
        if choice == 1:
            print("Adjust URL Due to HTML. Grabbing Jay Williams")
            count = "03"
        elif choice == 2:
            print("Adjust URL Due to HTML. Grabbing Jawad Williams")
            count = "04"
        elif choice == 3:
            print("Adjust URL Due to HTML. Grabbing Jalen Williams")
            count = "06"
        elif choice == 4:
            print("Adjust URL Due to HTML. Grabbing Jaylin Williams")
            count = "07"

    return count


def find_team(team_initials):
    """This method is used to receive initials from soup, and compare it to the list of initials:team names and
    return the teams full name to be used later in the output of team stats. """
    nba_teams = {
        "ATL": "Atlanta Hawks",
        "BOS": "Boston Celtics",
        "BRK": "Brooklyn Nets",
        "CHO": "Charlotte Hornets",
        "CHI": "Chicago Bulls",
        "CLE": "Cleveland Cavaliers",
        "DAL": "Dallas Mavericks",
        "DEN": "Denver Nuggets",
        "DET": "Detroit Pistons",
        "GSW": "Golden State Warriors",
        "HOU": "Houston Rockets",
        "IND": "Indiana Pacers",
        "LAC": "LA Clippers",
        "LAL": "Los Angeles Lakers",
        "MEM": "Memphis Grizzlies",
        "MIA": "Miami Heat",
        "MIL": "Milwaukee Bucks",
        "MIN": "Minnesota Timberwolves",
        "NOP": "New Orleans Pelicans",
        "NYK": "New York Knicks",
        "OKC": "Oklahoma City Thunder",
        "ORL": "Orlando Magic",
        "PHI": "Philadelphia 76ers",
        "PHO": "Phoenix Suns",
        "POR": "Portland Trail Blazers",
        "SAC": "Sacramento Kings",
        "SAS": "San Antonio Spurs",
        "TOR": "Toronto Raptors",
        "UTA": "Utah Jazz",
        "WAS": "Washington Wizards",
        "NJN": "New Jersey Nets",
        "VAN": "Vancouver Grizzlies",
        "CHH": "Charlotte Hornets",
        "SEA": "Seattle Supersonics",
        "SYR": "Syracuse Nationals",
        "STL": "St. Louis Hawks",
        "MNL": "Minneapolis Lakers",
        "PHW": "Philadelphia Warriors",
        "CIN": "Cincinnati Royals",
        "TOT": "Played for more than one team this season"
    }
    team_name = nba_teams[f'{team_initials}']
    return team_name


def find_player_season_stats():
    global team1, team2
    """This is the main method of this class and the core of the player search option for this program. It takes
    a name from the user_input_validation_player method, applies it to the translate_name method, and then asks
    for the year which is also validated, and then calls the web_scrape function with the variables for name and
    year from there we will extract specified data and then send it to the display_player_stats method. Also, this
    method works with the method get_multiple_teams in the event the player has played for more than one team,
    and allows us to add all the required information to the output. """
    name = user_input_validation_player()
    player = translate_name(name)
    # YEAR = '2024'
    while True:
        try:
            season_year_player = 2024
            # season_year_player = int(input("What year? (Ex. 2024 for the '2023-2024' season) *Only Accepts Seasons "
            #                                "after "
            #                                "1960*: "))
            if len(str(season_year_player)) != 4 or season_year_player < 1960:
                raise ValueError("Invalid input: Year must be 4 characters long and greater than or equal to 1971.")
        except ValueError as ve:
            print(ve)
        else:
            break  # Exit the loop if input is valid

    soup = web_scrape(season_year_player, player)
    #print(soup.prettify())
    try:
        row = soup.find("tr", id=f"per_game.{season_year_player}")
        # Extract season year
        season_year_element = row.find("th", {"data-stat": "season"}).a
    except AttributeError:
        print(f"Cannot find {name} stats for this year ({season_year_player})")
        print("\nPlease Ensure You are entering 'Y' on the right player's name. \nSome players have similar ID's "
              "based on same last name and similar spelling in their first names.")
        pass
    else:
        season_year = season_year_element.text.strip()
        print(f"\nSeason year: {season_year}")

        # Extract team names
        team_initials = row.find("td", {"data-stat": "team_id"}).text.strip()
        multiple_teams = False
        if team_initials == "TOT":
            multiple_teams = True
            teams = get_multiple_team(row)
            team1 = find_team(teams[0])
            team2 = find_team(teams[1])

        games_played = row.find("td", {"data-stat": "g"}).text.strip()
        points_per_game = row.find("td", {"data-stat": "pts_per_g"}).text.strip()
        field_goal_percentage = row.find("td", {"data-stat": "fg_pct"}).text.strip()
        rebound_per_game = row.find("td", {"data-stat": "trb_per_g"}).text.strip()
        ast_per_game = row.find("td", {"data-stat": "ast_per_g"}).text.strip()
        try:
            three_pt_perc = row.find("td", {"data-stat": "fg3_pct"})
            if three_pt_perc is not None:
                three_points_percentage = three_pt_perc.text.strip()
            else:
                three_points_percentage = "N/A"
                print("Warning: 'three_point_percentage' element not found.")
        except AttributeError:
            # Handle the case when 'row.find' raises an AttributeError (NoneType)
            three_points_percentage = "N/A"
            print("Error: Unable to retrieve 'three_point_percentage' element.")

        free_throw_percentage = row.find("td", {"data-stat": "ft_pct"}).text.strip()

        team_full_name = find_team(team_initials)
        multiple_team_full_name = f"{team1} and {team2}"
        # This creates a dictionary for the player's output if the 3pt was not a stat at the time
        if three_points_percentage == "N/A":
            player_stat = {
                'Name': name,
                'Team': team_full_name if not multiple_teams else multiple_team_full_name,
                "Games": games_played,
                "Points": points_per_game,
                "Total Rebounds": rebound_per_game,
                "Assists": ast_per_game,
                "Field Goal Percentage": field_goal_percentage,
                "Free Throw Percentage": free_throw_percentage
            }
        else:
            player_stat = {
                'Name': name,
                'Team': team_full_name if not multiple_teams else multiple_team_full_name,
                "Games": games_played,
                "Points": points_per_game,
                "Total Rebounds": rebound_per_game,
                "Assists": ast_per_game,
                "Field Goal Percentage": field_goal_percentage,
                "3-Point Field Goal Percentage": three_points_percentage,
                "Free Throw Percentage": free_throw_percentage
            }
        display_player_stats(player_data=player_stat,
                             team_full_name=team_full_name if not multiple_teams else multiple_team_full_name,
                             player_name=proper_name)
        input("\nEnter any key to continue.....")


def get_multiple_team(row):
    """This gets the names of multiple teams the player has played for that season IF they have more than one team
    they were a part of in the requested season, if not then this method isn't called for"""
    next_row1 = row.find_next_sibling("tr")
    next_row2 = next_row1.find_next_sibling("tr")
    # Extracting team initials
    next_team_initials1 = next_row1.find("td", {"data-stat": "team_id"}).text.strip()
    next_team_initials2 = next_row2.find("td", {"data-stat": "team_id"}).text.strip()
    return next_team_initials1, next_team_initials2


def display_player_stats(player_data, team_full_name, player_name):
    """This method is used to output player season stats"""

    print("Searching player database.....")
    player_name = f"\nPlayer: {player_name}"
    team_played_for = f"{team_full_name}"
    games_played = f"{player_data['Games'].strip()}"
    points = f"{player_data['Points'].strip()}"
    rebounds = f"{player_data['Total Rebounds'].strip()}"
    assists = f"{player_data['Assists'].strip()}"
    field_goal_pct = f"{player_data['Field Goal Percentage'].strip()}"
    three_point_pct = f"{player_data.get('3-Point Field Goal Percentage', '').strip()}"
    free_throw_pct = f"{player_data['Free Throw Percentage'].strip()}"
    if not player_data['Games'].strip():
        print("Could not find any valid data on this player. Either He is retired, or Your looking for another"
              "player with a similar name. Please Try Again.")
    else:
        print(f"{player_name}"
              f"\nHe plays/ed for the {team_played_for} this season."
              f"\nHe played in {games_played} games",
              f"\nScored {points} points per game",
              f"\nHad {rebounds} rebounds per game",
              f"\nHad {assists} assists per game",
              f"\nShot {field_goal_pct}% for Field Goals",
              f"\nShot {three_point_pct}% from 3-pt Range" if three_point_pct else "",
              f"\nShot {free_throw_pct}% from the Free-Throw Line")


def user_input_validation_player():
    """Validates user input for player name."""
    while True:
        try:
            name = input("\nName a player: ")
            if not name.replace(" ", "").replace("-", "").isalpha():
                raise ValueError("Invalid input: Please enter a valid name (letters and spaces only).")
        except ValueError as ve:
            print(ve)
        except KeyboardInterrupt:
            print("\nUser interrupted the input.")
        else:
            break  # Exit the loop if input is valid
    return name
