import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3
import numpy as np
from numpy import random

#load data (make sure you have downloaded database.sqlite)
with sqlite3.connect('C:/Users/nar29695/Documents/My created reports/database.sqlite') as con:
    countries = pd.read_sql_query("SELECT * from Country", con)
    leagues = pd.read_sql_query("SELECT * from League", con)
    matches = pd.read_sql_query("SELECT * from Match", con)
    players = pd.read_sql_query("SELECT * from Player", con)
    players_attributes = pd.read_sql_query("SELECT * from Player_Attributes", con)
    sqlite_sequences = pd.read_sql_query("SELECT * from sqlite_sequence", con)
    teams = pd.read_sql_query("SELECT * from Team", con)
    team_attributes = pd.read_sql_query("SELECT * from Team_Attributes", con)

#https://www.kaggle.com/hugomathien/soccer#database.sqlite look at this.

#Dataframe Total_Rows Total_Columns Columns.....

#Basically the country, its ID, and its name
#Country	11	2	id, name 

#Basically the league, its ID, the countries' ID it belongs to, and its name
#League	11	3	id, country_id, name

#It contains matches information starting with all IDs associated. Season represents the year. Stage I have no idea its kinda weird but most probably represents Season only.
#date represents the date of the match. MatchID, hometeamID, awayteamID, goals scored by home and away team. //home_player_X* contains information regarding the X position of 
# the player. home_player_Y* contains information regarding the Y position of the player. home_player_* contains information regarding the player?//-Not sure about this
# 
#Match	25979	115	id, country_id, league_id, season, stage, date, match_api_id, home_team_api_id, away_team_api_id, 
#   home_team_goal, away_team_goal, home_player_X1, home_player_X2, home_player_X3, home_player_X4, home_player_X5, 
#   home_player_X6, home_player_X7, home_player_X8, home_player_X9, home_player_X10, home_player_X11, away_player_X1, 
#   away_player_X2, away_player_X3, away_player_X4, away_player_X5, away_player_X6, away_player_X7, away_player_X8, 
#   away_player_X9, away_player_X10, away_player_X11, home_player_Y1, home_player_Y2, home_player_Y3, home_player_Y4,
#   home_player_Y5, home_player_Y6, home_player_Y7, home_player_Y8, home_player_Y9, home_player_Y10, home_player_Y11,
#   away_player_Y1, away_player_Y2, away_player_Y3, away_player_Y4, away_player_Y5, away_player_Y6, away_player_Y7,
#   away_player_Y8, away_player_Y9, away_player_Y10, away_player_Y11, home_player_1, home_player_2, home_player_3, 
#   home_player_4, home_player_5, home_player_6, home_player_7, home_player_8, home_player_9, home_player_10, home_player_11,
#   away_player_1, away_player_2, away_player_3, away_player_4, away_player_5, away_player_6, away_player_7, away_player_8,
#   away_player_9, away_player_10, away_player_11, goal, shoton, shotoff, foulcommit, card, cross, corner, possession, B365H,
#   B365D, B365A, BWH, BWD, BWA, IWH, IWD, IWA, LBH, LBD, LBA, PSH, PSD, PSA, WHH, WHD, WHA, SJH, SJD, SJA, VCH, VCD, VCA, GBH, GBD, GBA, BSH, BSD, BSA


#Player	11060	7	id, player_api_id, player_name, player_fifa_api_id, birthday, height, weight

#Player_Attributes	183978	42	id, player_fifa_api_id, player_api_id, date, overall_rating, potential,
#   preferred_foot, attacking_work_rate, defensive_work_rate, crossing, finishing, heading_accuracy, 
#   short_passing, volleys, dribbling, curve, free_kick_accuracy, long_passing, ball_control, acceleration,
#   sprint_speed, agility, reactions, balance, shot_power, jumping, stamina, strength, long_shots, 
#   aggression, interceptions, positioning, vision, penalties, marking, standing_tackle, sliding_tackle,
#   gk_diving, gk_handling, gk_kicking, gk_positioning, gk_reflexes

#sqlite_sequence	7	2	name, seq

#Team	299	5	id, team_api_id, team_fifa_api_id, team_long_name, team_short_name

#Team_Attributes	1458	25	id, team_fifa_api_id, team_api_id, date, buildUpPlaySpeed,
#   buildUpPlaySpeedClass, buildUpPlayDribbling, buildUpPlayDribblingClass, buildUpPlayPassing,
#   buildUpPlayPassingClass, buildUpPlayPositioningClass, chanceCreationPassing, 
#   chanceCreationPassingClass, chanceCreationCrossing, chanceCreationCrossingClass,
#   chanceCreationShooting, chanceCreationShootingClass, chanceCreationPositioningClass, 
#   defencePressure, defencePressureClass, defenceAggression, defenceAggressionClass, defenceTeamWidth, defenceTeamWidthClass, defenceDefenderLineClass


print(matches['shoton'])






#EASIER WAY TO MANIPULATE AND FIX DATA.
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3
import matplotlib.pyplot as plt


path = "C:/Users/nar29695/Documents/My created reports/"  #Insert path here
database = path + 'database.sqlite'

#https://www.kaggle.com/jiezi2004/soccer#possession_detail.csv ALL THE MISSING COLUMNS ARE HERE

conn = sqlite3.connect(database)

tables = pd.read_sql("""SELECT *
                        FROM sqlite_master
                        WHERE type='table';""", conn)

countries = pd.read_sql("""SELECT *
                        FROM Country;""", conn)

leagues = pd.read_sql("""SELECT *
                        FROM League
                        JOIN Country ON Country.id = League.country_id;""", conn)                        
teams = pd.read_sql("""SELECT *
                        FROM Team
                        ORDER BY team_long_name;""", conn)
detailed_matches = pd.read_sql("""SELECT Match.id, 
                                        Country.name AS country_name, 
                                        League.name AS league_name, 
                                        season, 
                                        stage, 
                                        date,
                                        HT.team_long_name AS  home_team,
                                        AT.team_long_name AS away_team,
                                        home_team_goal, 
                                        away_team_goal                                        
                                FROM Match
                                JOIN Country on Country.id = Match.country_id
                                JOIN League on League.id = Match.league_id
                                LEFT JOIN Team AS HT on HT.team_api_id = Match.home_team_api_id
                                LEFT JOIN Team AS AT on AT.team_api_id = Match.away_team_api_id
                                ORDER by date;""", conn)
print(detailed_matches)