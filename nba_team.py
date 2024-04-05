"""Imports needed"""
import requests
from bs4 import BeautifulSoup

global URL


def get_old_conference_data(year, conference):
    """this is where we get data on the conferences for our team requests and then process it into a list with all the
    specified information attached for each respective team. This is more for the older teams i.e 1971 to 2016"""
    global conference_soup
    URL = f"https://www.basketball-reference.com/leagues/NBA_{year}.html"
    # print(URL)
    response = requests.get(url=URL)
    data = response.text

    soup = BeautifulSoup(data, "html.parser")
    if int(year) >= 2016:
        team_data_dict = modern_team_check(conference, soup)
        return team_data_dict
    else:
        if conference == 'E':
            conference_name = "Eastern"
        else:
            conference_name = "Western"
        try:
            # Assuming you've already scraped the data and stored it in conference_soup
            conference_soup = soup.find(id=f"divs_standings_{conference}")
        except AttributeError:
            print("Checking other database")
        else:
            conference_soup = soup.find(id=f"divs_standings_{conference}")
        team_rows = conference_soup.select('tbody tr.full_table')
        team_names = []
        for row in team_rows:
            team_element = row.find('th', class_='left')
            team = team_element.get_text().strip("*")
            team_names.append(team)
        # Initialize an empty list to store team data dictionaries
        team_data_list = []
        # Checks the "Seed" ranking and gives it a number formatted from this standings list
        standings = ['(1)', '(2)', '(3)', '(4)', '(5)', '(6)', '(7)', '(8)', '(9)', '(10)', '(11)', '(12)', '(13)',
                     '(14)', '(15)', '(1)', '(2)', '(3)', '(4)', '(5)', '(6)', '(7)', '(8)', '(9)', '(10)', '(11)',
                     '(12)', '(13)', '(14)', '(15)']
        # Iterate through each team's data and add it to the list
        for i, row in enumerate(team_rows):
            columns = row.find_all("td")
            team_data = {
                "Team Name": team_names[i].strip(),  # Use the corresponding team name
                "Standing": standings[i].strip('()'),
                "Conference": conference_name,
                "Wins": int(columns[0].text),
                "Loss": int(columns[1].text),
                "W/L%": float(columns[2].text),
                "GB": columns[3].text.strip(),
                "PS/G": float(columns[4].text),
                "PA/G": float(columns[5].text),
                "SRS": float(columns[6].text)
            }
            team_data_list.append(team_data)
        team_data_dict = {team["Team Name"]: team for team in
                          team_data_list}  # Append the team data dictionary to the list
        return team_data_dict


def modern_team_check(conference, soup):
    """This handles the same as get_old_conference_data except focuses on modern teams and recent seasons. This was
    because basketball references format changed from 2016 onward compared to 2015."""

    global conference_soup
    if conference == 'E':
        conference_name = "Eastern"
    else:
        conference_name = "Western"
    try:
        # Assuming you've already scraped the data and stored it in conference_soup
        conference_soup = soup.find(id=f"confs_standings_{conference}")
    except AttributeError:
        print("Checking other database")
    else:
        conference_soup = soup.find(id=f"confs_standings_{conference}")
    team_rows = conference_soup.find_all("tr")[1:]  # Skip the header row
    team_names = []
    for team in team_rows:
        team_names.append(team.find("a").text)
    # Initialize an empty list to store team data dictionaries
    team_data_list = []

    standings = ['(1)', '(2)', '(3)', '(4)', '(5)', '(6)', '(7)', '(8)', '(9)', '(10)', '(11)', '(12)', '(13)',
                 '(14)', '(15)', '(1)', '(2)', '(3)', '(4)', '(5)', '(6)', '(7)', '(8)', '(9)', '(10)', '(11)',
                 '(12)', '(13)', '(14)', '(15)']
    # Iterate through each team's data and add it to the list
    for i, row in enumerate(team_rows):
        columns = row.find_all("td")
        team_data = {
            "Team Name": team_names[i].strip(),  # Use the corresponding team name
            "Standing": standings[i].strip('()'),
            "Conference": conference_name,
            "Wins": int(columns[0].text),
            "Loss": int(columns[1].text),
            "W/L%": float(columns[2].text),
            "GB": columns[3].text.strip(),
            "PS/G": float(columns[4].text),
            "PA/G": float(columns[5].text),
            "SRS": float(columns[6].text)
        }
        team_data_list.append(team_data)
    team_data_dict = {team["Team Name"]: team for team in
                      team_data_list}  # Append the team data dictionary to the list
    return team_data_dict


def choose_team():
    """Gets the user choice on team"""
    team = input("Choose an NBA Team: ")
    return team


def get_user_choice(nba_team_data, year, team):
    """Checks Team and Season and gives you the stats based on user choice"""
    season_year = int(year)
    season_output = f"{season_year} - {season_year + 1}"
    if team not in nba_team_data:
        print("Sorry, this entry is invalid. Possible Reasons:\n"
              "* Misspelled the City/Team Name \n"
              "* Entered a Team Name that didn't exist that season \n"
              "* Entered a Team Name and The City which wasn't correct for that season \n"
              "* We will transfer back to the query select, You can try to enter a new name once you "
              "re-prompt to go to the Team Database")
        return
    else:
        print(
            f"We will give you the following options for the {team} in the {season_output} season. Here are the "
            f"options: "
            f"\nStanding(S)"
            f"\nWins(W)"
            f"\nLosses(L)"
            f"\nGames Back(GB)"
            f"\nPoints per Game (PS)"
            f"\nPoints Against per Game(PA)"
            f"\nOr enter 'All' to get all the information for your team")
        choice = input("Choose which stats you would like to know? ")
        if choice == 'S':
            print(
                f"The {team} is/was at the {nba_team_data[f'{team}']['Standing']} seed in their conference for the"
                f" {season_output} season")

        if choice == 'W':
            print(f"The {team} has {nba_team_data[f'{team}']['Wins']} wins in the {season_output} season")

        elif choice == 'L':
            print(f"The {team} has {nba_team_data[f'{team}']['Loss']} losses in the {season_output} season")

        elif choice == 'GB':
            print(f"The {team} are {nba_team_data[f'{team}']['Games Back']} games back from First Place in the "
                  f"{nba_team_data[f'{team}']['Conference']} in the {season_output} season")

        elif choice == 'PS':
            print(f"The {team} has scored {nba_team_data[f'{team}']['PS/G']} points per game in "
                  f"the {season_output} season")

        elif choice == 'PA':
            print(f"The {team} has allowed {nba_team_data[f'{team}']['PA/G']}"
                  f" points per game+ in the {season_output} season")

        elif choice == 'All':
            output_team_data(nba_team_data=nba_team_data, team=team, year=year)

    roster = input("Would you like to see the team's roster for this season? (Y/N): ").upper()
    if roster == "Y":
        get_roster(team=team, year=season_year)
    else:
        print("Going to Main Menu")
        return


def output_team_data(nba_team_data, team, year):
    """This organizes ALL the stats so if the user wants to see everything at once, this will run."""
    season_year = int(year)
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Data for the {season_year - 1} - {season_year} NBA Season")
    print(f"Team Name: {team}")
    print(f"Standing: {nba_team_data[f'{team}']['Standing']}")
    print(f"Conference: {nba_team_data[f'{team}']['Conference']}")
    print(f"Wins: {nba_team_data[f'{team}']['Wins']}")
    print(f"Losses: {nba_team_data[f'{team}']['Loss']}")
    print(
        f"Win-Loss Percentage (W/L%): {nba_team_data[f'{team}']['W/L%']:.3f}")
    print(f"Games Back: {nba_team_data[f'{team}']['GB']}")
    print(
        f"Points Scored per Game (PS/G): {nba_team_data[f'{team}']['PS/G']:.1f}")
    print(f"Points Allowed per Game (PA/G): {nba_team_data[f'{team}']['PA/G']:.1f}")


def get_roster(team, year):
    """This is where we request for teams and use soup to find them all, so we can access their data. Then, once it
    finds the right team, it will print out in an organized fashion all players and relevant information regarding each
    """
    initials = get_initials_from_team_name(team_name=team)
    # value = nba_player.NbaPlayer.find_team(initials)

    roster_url = f"https://www.basketball-reference.com/teams/{initials}/{year}.html"
    response = requests.get(url=roster_url)
    data = response.text
    roster_soup = BeautifulSoup(data, "html.parser")
    pos = roster_soup.find_all("td", {"data-stat": "pos"})
    height = roster_soup.find_all("td", {"data-stat": "height"})
    weight = roster_soup.find_all("td", {"data-stat": "weight"})
    b_date = roster_soup.find_all("td", {"data-stat": "birth_date"})
    b_country = roster_soup.find_all("td", {"data-stat": "birth_country"})
    exp = roster_soup.find_all("td", {"data-stat": "years_experience"})
    col = roster_soup.find_all("td", {"data-stat": "college"})

    positions = [tag.text for tag in pos]
    heights = [tag.text for tag in height]
    weights = [tag.text for tag in weight]
    birthdays = [tag.text for tag in b_date]
    birth_country = [tag.text for tag in b_country]
    experience_years = [tag.text for tag in exp]
    college = [tag.text for tag in col]
    name_rows = roster_soup.select('tbody tr')

    roster_players = []
    # Extract player names from each row
    for row in name_rows:
        player_name_element = row.find('td', class_='left')
        player_name = player_name_element.get_text()
        roster_players.append(player_name)
    roster_player_names = remove_duplicates(names=roster_players)
    fixed_player_names = [name.replace('\xa0', ' ').replace('(TW)', '') for name in roster_player_names]
    player_dicts = []
    for name, position, height, weight, birthday, birth_country, experience, college in zip(fixed_player_names,
                                                                                            positions, heights,
                                                                                            weights,
                                                                                            birthdays,
                                                                                            birth_country,
                                                                                            experience_years,
                                                                                            college):
        player_dict = {
            'name': name,
            'position': position,
            'height': height,
            'weight': weight,
            'birthday': birthday,
            'country': birth_country.upper(),
            'experience': experience,
            'college': college
        }
        player_dicts.append(player_dict)

    print(f"\n\t{team} roster for the {year - 1} - {year} season")
    print(
        f"{'Name':<20} {'Position':<10} {'Height':<10} {'Weight':<10} {'Birthday':<20} {'Country':<10} "
        f"{'Experience (Years)':<20} {'College'}")

    for player_dict in player_dicts:
        formatted_name = f"{player_dict['name'][:20]:<20}"  # :<20 is me limiting to specified characters
        print(
            f"{formatted_name:<20} {player_dict['position']:<10} {player_dict['height']:<10} "
            f"{player_dict['weight']:<10}"
            f" {player_dict['birthday']:<20} {player_dict['country']:<10} {player_dict['experience']:<20}"
            f" {player_dict['college']}")


def remove_duplicates(names):
    """This allows me to remove any duplicate names which was a reaction to a bug I encountered and this was a quick
    but efficient fix to that bug"""
    seen = set()
    return [x for x in names if not (x in seen or seen.add(x))]


def get_initials_from_team_name(team_name):
    """This uses the Team names to get the Initials and returns it."""
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
    for initials, name in nba_teams.items():
        if name == team_name:
            return initials
    return "Team name not found"
