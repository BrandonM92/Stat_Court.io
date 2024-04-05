# StatCourt Application
# Programmer: Brandon Mathews
# Purpose : Act as a central hub for all information regarding NBA basketball.
# Date Started: 3/1/2024 Date Finished: 3/20/2024
import injury_report
import nba_team
import nba_player
import awards
import last_5_days
import bettingcorner

logo = r"""
 $$$$$$\    $$\                 $$\      $$$$$$\                                  $$\     ©
$$  __$$\   $$ |                $$ |    $$  __$$\                                 $$ |    
$$ /  \__|$$$$$$\    $$$$$$\  $$$$$$\   $$ /  \__| $$$$$$\  $$\   $$\  $$$$$$\  $$$$$$\   
\$$$$$$\  \_$$  _|   \____$$\ \_$$  _|  $$ |      $$  __$$\ $$ |  $$ |$$  __$$\ \_$$  _|  
 \____$$\   $$ |     $$$$$$$ |  $$ |    $$ |      $$ /  $$ |$$ |  $$ |$$ |  \__|  $$ |    
$$\   $$ |  $$ |$$\ $$  __$$ |  $$ |$$\ $$ |  $$\ $$ |  $$ |$$ |  $$ |$$ |        $$ |$$\ 
\$$$$$$  |  \$$$$  |\$$$$$$$ |  \$$$$  |\$$$$$$  |\$$$$$$  |\$$$$$$  |$$ |        \$$$$  |
 \______/    \____/  \_______|   \____/  \______/  \______/  \______/ \__|         \____/
"""

VERSION = "Version 2.3"


def get_team_data():
    while True:
        try:
            YEAR = int(input("Choose a year (1971 or higher): "))
            if len(str(YEAR)) != 4 or YEAR < 1971 or YEAR > 2025:
                raise ValueError("Invalid input: Year must be 4 characters long and must be from the 1971 season"
                                 " until this year")
        except ValueError as ve:
            print(ve)
        else:
            break  # Exit the loop if input is valid

        # Now you have a validated proper input in the 'YEAR' variable
    print(f"Validated input: {YEAR}")
    # Create an empty list to store team data dictionaries
    if YEAR >= 2016:
        east_conference = nba_team.get_old_conference_data(year=YEAR, conference="E")
        west_conference = nba_team.get_old_conference_data(year=YEAR, conference="W")
        nba_team_data = {**east_conference, **west_conference}
        team = nba_team.choose_team()
        nba_team.get_user_choice(nba_team_data=nba_team_data, year=YEAR, team=team)
    else:
        east_conference = nba_team.get_old_conference_data(year=YEAR, conference="E")
        west_conference = nba_team.get_old_conference_data(year=YEAR, conference="W")
        nba_team_data = {**east_conference, **west_conference}
        team = nba_team.choose_team()
        nba_team.get_user_choice(nba_team_data=nba_team_data, year=YEAR, team=team)


def get_player_data():
    nba_player.find_player_season_stats()


def get_player_awards():
    awards.find_player_awards()


def get_betting_corner():
    print("\nWelcome to the StatCourt Betting Corner 🏀💰. Here you have access to the following options: "
          "\nA) Check a players last 10 games stats"
          "\nB) Check which stats the player has hit within their team's last 10 games by percentage:"
          "\n 100%, \t80%, \t60%, \t40%."
          "\nC) StatCourt offers a unique player prop bet checker:"
          "\nYou type in player props for each stat: Pts,3pts,Ast,Rbs,Stl,Blks and we will inform you of how"
          "\nmany games the player has reached those numbers or better this season."
          "\nD) Lastly StatCourt also employs an Injury Report Checker courtesy of CBSsports.com, "
          "where it will see if the player you are searching for"
          "\n is on today's injury report. Note: This list is updated frequently, check closer to game time for "
          "\naccurate information")
    input("\nEnter any key to continue...")

    print("\nIf you or someone you know has a serious problem with gambling, call 1-800-GAMBLER.")
    selection = input("\nWhich part would you like to go to?: \nA) All Sections"
                      "\nB) To Access Just The Injury Report Check"
                      "\nC) To Access Just The Player Prop Bet Check"
                      "\nD) To Access Just the Last 10 Probability Prop Check"
                      "\nE) to end program: ").upper()
    if selection == "A":
        print("\nEntering: Betting Corner - Player Check (A)")
        soup = bettingcorner.scrape_stats()
        if soup is None:
            print('\nGoing Back To Main Menu.')
            return
        else:
            print("\nEntering: Betting Corner - Last 10 Days/Probability Check/Injury Check (B)(D)")
            bettingcorner.last_10_days(soup=soup, option="2")
            print("\nEntering: Betting Corner - Player Prop Bet Check(C)")
            bettingcorner.bet_check(bettingcorner.player_name)

    if selection == "B":
        print(
            "\nWelcome to StatCourt Injury Report 🏀❤️‍🩹. Please Remember if the name you enter doesn't process it's "
            "either "
            "\nbecause they are not listed on CBS.com Injury Report OR the name was misspelled. "
            "Fortunately, For only "
            "\nthis section if you have trouble, TRY to use their first initial then period and "
            "then last name to search. "
            "\nEX: J. Embiid")
        injury_report.get_injury_report("")
    if selection == "C":
        print("\nWelcome to Stat Court Player Prop Bet Check.")
        bettingcorner.bet_check(bet_check_player_name="")
    if selection == "D":
        print("\nWelcome to the Stat Court Last 10 Probability Check")
        soup = bettingcorner.scrape_stats()
        bettingcorner.last_ten_day_prop_check(soup=soup)
    if selection == "E":
        return


def main():
    print(logo)
    print("\n'Where the Stats meet the Hardwood' 📈📊")
    print("\nDesigned by Brandon Mathews")
    print(VERSION)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    input("Enter Any Key to go to main menu....")
    print(
        "\nUnderstand this is a student project assignment and will not be used/abused during and outside of "
        "\nthis assignment, for all users here are links to their policies on web scraping: "
        "\nhttps://www.sports-reference.com/data_use.html"
        "\nhttps://www.sports-reference.com/bot-traffic.html")
    print(
        "Do not use this program more than 10 times per any given minute ⛔, this is to both prevent any affect to the "
        "website as well as being unnecessary. ")
    print("\nMAIN MENU: ")
    choice = input("\nFor your first query, "
                   "\nDo you wish to access our Team Database(T),"
                   "\nPlayer Database(P),"
                   "\nPlayer Awards Database(A)"
                   "\nStat Predictor/Last 5 Games(L), "
                   "\nBetting Corner (B) "
                   "\nTo End Program (E) or Any Other Key?").upper()
    while choice == 'T' or choice == 'P' or choice == 'A' or choice == 'L' or choice == 'E' or choice == 'B':
        if choice == 'T':
            print("\nAccessing Team Database ⛹, Please wait.....")
            get_team_data()
            print("\nMAIN MENU: ")
            choice = input("\nFor your next query, "
                           "\nDo you wish to access our Team Database(T),"
                           "\nPlayer Database(P),"
                           "\nPlayer Awards Database(A)"
                           "\nStat Predictor/Last 5 Games(L), "
                           "\nBetting Corner (B) "
                           "\nTo End Program (E) or Any Other Key?").upper()
        elif choice == 'P':
            print("\nAccessing Active Player Database ⛹, Please wait.......")
            get_player_data()
            print("\nMAIN MENU: ")
            choice = input("\nFor your next query, "
                           "\nDo you wish to access our Team Database(T),"
                           "\nPlayer Database(P),"
                           "\nPlayer Awards Database(A)"
                           "\nStat Predictor/Last 5 Games(L), "
                           "\nBetting Corner (B) "
                           "\nTo End Program (E) or Any Other Key?").upper()
        elif choice == 'A':
            """This is for player awards"""
            print("Transferring, to our Player Awards Database 🏆. Note: This will show all awards for current players"
                  "as of the All-Star break for the 2024 season.")
            get_player_awards()
            print("\nMAIN MENU: ")
            choice = input("\nFor your next query, "
                           "\nDo you wish to access our Team Database(T),"
                           "\nPlayer Database(P),"
                           "\nPlayer Awards Database(A)"
                           "\nStat Predictor/Last 5 Games(L), "
                           "\nBetting Corner (B) "
                           "\nTo End Program (E) or Any Other Key?").upper()

        elif choice == 'L':
            """This is to look up Last 5 games or Stat Predictions 🔮"""
            last_5_days.choose_option()
            print("\nMAIN MENU: ")
            choice = input("\nFor your next query, "
                           "\nDo you wish to access our Team Database(T),"
                           "\nPlayer Database(P),"
                           "\nPlayer Awards Database(A)"
                           "\nStat Predictor/Last 5 Games(L), "
                           "\nBetting Corner (B) "
                           "\nTo End Program (E) or Any Other Key?").upper()

        elif choice == 'B':
            """This is where we go to check player props and see last 🔟 days of a player stats"""
            get_betting_corner()
            print("\nMAIN MENU: ")
            choice = input("\nFor your next query, "
                           "\nDo you wish to access our Team Database(T),"
                           "\nPlayer Database(P),"
                           "\nPlayer Awards Database(A)"
                           "\nStat Predictor/Last 5 Games(L), "
                           "\nBetting Corner (B) "
                           "\nTo End Program (E or Any Other Key)?").upper()

        elif choice == 'E':
            print("\nEnding the program.....")
            break
    else:
        pass


main()
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("\nThanks for using StatCourt. © B_Statistics 2024")
