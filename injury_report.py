import requests
from bs4 import BeautifulSoup
from datetime import datetime

today = datetime.today().date()


def get_injury_report(player):
    """This is where we request and search soup for all the data in the injury table. Then we use other methods to
    search and output data from it."""
    url = f"https://www.cbssports.com/nba/injuries/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup.prettify())
    player_data = {}
    player_data_2 = {}
    rows = soup.find_all('tr', class_='TableBase-bodyTr')
    # Extract data for each player and store it in the dictionary
    for row in rows:
        short_player_name = row.find('span', class_='CellPlayerName--short').text.strip()
        player_name = row.find('span', class_='CellPlayerName--long').text.strip()
        position = row.find_all('td')[1].text.strip()
        updated_date = row.find('span', class_='CellGameDate').text.strip()
        injury = row.find_all('td')[3].text.strip()
        injury_status = row.find_all('td')[4].text.strip()
        player_data[player_name] = {
            'Player Name': player_name,
            'Position': position,
            'Updated Date': updated_date,
            'Injury': injury,
            'Injury Status': injury_status
        }
        player_data_2[short_player_name] = {
            'Player Name': player_name,
            'Position': position,
            'Updated Date': updated_date,
            'Injury': injury,
            'Injury Status': injury_status
        }
    if player == "":
        get_player_and_display(player_data, player_data_2, "")
    else:
        get_player_and_display_once(player_data, player_data_2, player)


def get_player_and_display_once(player_data, player_data_2, player_name):
    """This is for the situation where you have gone through each other section of betting corner, this will process
    the player's name already, and you just hit Y or N if you want to see the result of the search."""
    choice = input(f"Would you like to check if a player is on the injury report for {today}? ").upper()
    if choice == "Y":
        print("\nSearching for any possible lists for the player on today's injury report")
        user_input = player_name

        # Check if the input matches a player name
        if user_input in player_data:
            print(f"Player Name: {player_data[user_input]['Player Name']}")
            print(f"Position: {player_data[user_input]['Position']}")
            print(f"Updated Date: {player_data[user_input]['Updated Date']}")
            print(f"Injury: {player_data[user_input]['Injury']}")
            print(f"Injury Status: {player_data[user_input]['Injury Status']}")

        elif user_input in player_data_2:
            print(f"Player Name: {player_data_2[user_input]['Player Name']}")
            print(f"Position: {player_data_2[user_input]['Position']}")
            print(f"Updated Date: {player_data_2[user_input]['Updated Date']}")
            print(f"Injury: {player_data_2[user_input]['Injury']}")
            print(f"Injury Status: {player_data_2[user_input]['Injury Status']}")

        else:
            print(f"Player '{user_input}' not found in the table.")
            print(f"Either {user_input} is not on the Injury Report or check the spelling.")

    else:
        print("Moving On.")


def get_player_and_display(player_data, player_data_2, player_name):
    """This checks both the F. LastName and First Last Name formats and outputs the injury report in an organized format
    using our player_data from our web-scrape and soup search. This is used when the player requests specifically
    this section during the main query prompt."""
    go_again = True
    while go_again:
        if player_name == "":
            user_input = input("Enter a player name: ").title()
            player_name = user_input
        else:
            user_input = player_name
        if user_input in player_data:
            print(f"Player Name: {player_data[user_input]['Player Name']}")
            print(f"Position: {player_data[user_input]['Position']}")
            print(f"Updated Date: {player_data[user_input]['Updated Date']}")
            print(f"Injury: {player_data[user_input]['Injury']}")
            print(f"Injury Status: {player_data[user_input]['Injury Status']}")
            go_again = False  # Exit the loop after displaying info
        elif user_input in player_data_2:
            print(f"Player Name: {player_data_2[user_input]['Player Name']}")
            print(f"Position: {player_data_2[user_input]['Position']}")
            print(f"Updated Date: {player_data_2[user_input]['Updated Date']}")
            print(f"Injury: {player_data_2[user_input]['Injury']}")
            print(f"Injury Status: {player_data_2[user_input]['Injury Status']}")
            choice = input("Check Another Player? (Y/N): ")
            if choice.lower() == "y":
                player_name = ""  # Reset player_name for next iteration
            else:
                go_again = False  # Exit the loop
        else:
            print(f"Player '{user_input}' not found in the table. Check the spelling.")
            choice = input("Check Another Player? (Y/N): ")
            if choice.lower() == "y":
                player_name = ""  # Reset player_name for next iteration
            else:
                go_again = False  # Exit the loop

    print("\nLeaving Injury Report...")