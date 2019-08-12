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
