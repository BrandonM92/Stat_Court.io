import requests
from bs4 import BeautifulSoup
import nba_player


def translate_name(name):
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
        jr = "N/A"
        return initial, username, jr


def web_scrape_awards(YEAR, player):
    """This is where we scrape Awards information"""
    count = "01"
    choice = "N"
    if player[2] != "N/A":
        count = "02"
    elif player[2] == "N/A":
        count = "01"
    while choice == 'N':
        count = nba_player.player_name_outdated_html(count,player)
        URL = f"https://www.basketball-reference.com/players/{player[0]}/{player[1]}{count}/gamelog/{YEAR}"
        # print(URL)
        response = requests.get(url=URL)
        data = response.text
        try:
            soup = BeautifulSoup(data, "html.parser")
            title = soup.select_one("#meta > div:nth-child(2) > h1 > span").text
        except AttributeError:
            print("ERROR:")
            return
        else:
            name = " ".join(title.split()[:2])
            print(f"\nChecking all entries that could potentially match {name}.")
            choice = input(f"\nWere you looking for stats on {name}? Y/N: ")
            if choice == 'N':
                count = int(count) + 1
                count = str(f"0{count}")
    else:
        print(f"\nChecking for {name} player awards as of the {YEAR} season")
        return soup


def find_player_awards():
    """This is where we use the name entered and check the soup for any players and gets their awards if any"""
    name = user_input_validation_awards()
    player = translate_name(name)
    YEAR = "2024"  # We do 2024 so it gives the most recent awards
    if int(YEAR) > 2015:
        soup = web_scrape_awards(YEAR, player)
        try:
            a_tags = soup.select('#bling a')
        except AttributeError:
            print("Could not locate player, returning to main menu....")
        else:
            if not a_tags:
                print("\nThis player hasn't won any awards as of the 2024 NBA Season")
            else:
                for a_tag in a_tags:
                    print(a_tag.text.strip())
                    input("Enter to move on to the main query")


def user_input_validation_awards():
    """Validates user input"""
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
