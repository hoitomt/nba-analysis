"""
Parse Results that look like this:
0   ,1  ,2 ,3   ,4  ,5  ,6  ,7  ,8    ,9   ,10   ,11,12
Date,Rot,VH,Team,1st,2nd,3rd,4th,Final,Open,Close,ML,2H
1028,501,V,Cleveland,28,22,13,22,85,179.5,182.5,220,93.5
1028,502,H,Boston,22,21,24,23,90,7,6,-260,5
"""

import csv
import glob
import os

data_dir = "/Users/mhoitomt/Desktop/nba_game_data"

def new_game():
    return {
        'date_code': None,
        'home_team': None,
        'visiting_team': None,
        'home_team_score': 0,
        'visiting_team_score': 0,
        'spread_open': None,
        'spread_close': None,
        'total_open': 0,
        'total_close': 0,
        'money_line': 0,
        'spread_result': None,
        'total_result': None,
        'money_line_result': None,
    }

def create_game_from_rows(row_first, row_second):
    if row_first[2] == 'H':
        row_home = row_first
        row_visiting = row_second
    else:
        row_home = row_second
        row_visiting = row_first

    if row_home[9].lower() in ['pk', '']:
        row_home[9] = 0

    if row_visiting[9].lower() in ['pk', '']:
        row_visiting[9] = 0

    if row_home[10].lower() in ['pk', '']:
        row_home[10] = 0

    if row_visiting[10].lower() in ['pk', '']:
        row_visiting[10] = 0

    # If the value is > 50, assume it to be a total, else a spread
    # The spreads can move between row 1 and 2, which means
    # the total can also move
    if float(row_home[9]) > 100:
        total_open = float(row_home[9])
        spread_open = float(row_visiting[9])
    else:
        spread_open = float(row_home[9]) * -1
        total_open = float(row_visiting[9])
    print(row_home)
    if float(row_home[10]) > 100:
        total_close = float(row_home[10])
        spread_close = float(row_visiting[10])
    else:
        # The spread is listed on the favored team.
        # The spread will always be in relation to the home team.
        spread_close = float(row_home[10]) * -1
        total_close = float(row_visiting[10])

    game = new_game()
    game['date_code'] = row_home[0]
    game['home_team'] = row_home[3]
    game['visiting_team'] = row_visiting[3]
    game['home_team_score'] = int(row_home[8])
    game['visiting_team_score'] = int(row_visiting[8])
    game['spread_open'] = spread_open
    game['spread_close'] = spread_close
    game['total_open'] = total_open
    game['total_close'] = total_close

    if spread_close < 0:
        # Home Team Favored
        if (game['home_team_score'] + spread_close) > game['visiting_team_score']:
            game['spread_result'] = 'win'
        else:
            game['spread_result'] = 'loss'
    else:
        # Visiting Team favored
        if (game['visiting_team_score'] - spread_close) > game['home_team_score']:
            game['spread_result'] = 'win'
        else:
            game['spread_result'] = 'loss'

    if (game['home_team_score'] + game['visiting_team_score']) > game['total_close']:
        game['total_result'] = 'over'
    else:
        game['total_result'] = 'under'

    return game

def list_files():
    files = glob.glob(f"{data_dir}/*.csv")
    for filename in files:
        print(filename)
        game_data = parse_csv_file(filename)
        filename_without_ext = os.path.basename(filename).split('.')[0]
        write_game_data(filename_without_ext, game_data)

def parse_csv_file(filename):
    games = []
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        count = 1
        row_first = None
        for row in csvreader:
            if len(row) < 12:
                continue

            if count % 2 == 0:
                game = create_game_from_rows(row_first, row)
                # print(game)
                # print(f"Game Result: {game['home_team_score']} - {game['visiting_team_score']} || {game['spread_close']} | {game['spread_result']} | {game['total_close']} | {game['total_result']}")
                games.append(game)
            else:
                row_first = row
            count += 1

        # get total number of rows
        print("Total no. of rows: %d"%(csvreader.line_num))
    return games

def write_game_data(filename, games):
    file_name_parts = filename.split('_')
    first_year = file_name_parts[2]
    second_year = f"20{file_name_parts[3]}"
    season = filename.replace('nba_odds_', '')

    output_filename = f"{data_dir}/coallated_data/{filename}_coallated.csv"
    with open(output_filename, 'w') as outputfile:
        outputfile.write('season,date,visiting_team,home_team,visiting_team_score,home_team_score,spread_open,spread_close,total_open,total_close,spread_result_home_team,total_result\n')
        for game in games:
            date_code = game['date_code']
            day = date_code[-2:]
            month = date_code[:-2]
            int_month = int(month)
            int_day = int(day)
            if int_month >= 9:
                date_string = f"{first_year}-{int_month:02d}-{int_day:02d}"
            else:
                date_string = f"{second_year}-{int_month:02d}-{int_day:02d}"

            outputfile.write(f"{season},{date_string},{game['visiting_team']},{game['home_team']},{game['visiting_team_score']},{game['home_team_score']},{game['spread_open']},{game['spread_close']},{game['total_open']},{game['total_close']},{game['spread_result']},{game['total_result']}\n")

if __name__ == "__main__":
  list_files()
