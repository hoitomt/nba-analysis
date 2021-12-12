## Query

```
pipenv run csvsql --query "SELECT * FROM nba_odds_2018_19_coallated" ~/Desktop/nba_game_data/coallated_data/nba_odds_2018_19_coallated.csv
```

## Sqlite3

Create games table

```
CREATE TABLE IF NOT EXISTS games (
  date TEXT,
  visiting_team TEXT,
  home_team TEXT,
  visiting_team_score INT,
  home_team_score INT,
  spread_open REAL,
  spread_close REAL,
  total_open REAL,
  total_close REAL,
  spread_result_home_team TEXT ,
  total_result TEXT,
  UNIQUE(date,visiting_team,home_team)
);
```

Example Insert

```
INSERT INTO games (date,visiting_team,home_team,visiting_team_score,home_team_score,spread_open,spread_close,total_open,total_close,spread_result_home_team,total_result) VALUES ('2018-10-16','Philadelphia','Boston',87,105,-5.0,-4.5,208.5,211.5,'win','under');
```

Import Data

```
.mode csv
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2007_08_coallated.csv games
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2008_09_coallated.csv games
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2009_10_coallated.csv games
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2010_11_coallated.csv games
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2011_12_coallated.csv games
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2012_13_coallated.csv games
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2013_14_coallated.csv games
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2014_15_coallated.csv games
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2015_16_coallated.csv games
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2016_17_coallated.csv games
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2017_18_coallated.csv games
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2018_19_coallated.csv games
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2019_20_coallated.csv games
.import /Users/mhoitomt/Desktop/nba_game_data/coallated_data/nba_odds_2020_21_coallated.csv games
