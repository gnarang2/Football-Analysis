#Install all the required libraries here.
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import sqlite3
from os import listdir
from os.path import isfile, join

#load data (make sure you have downloaded database.sqlite)
with sqlite3.connect('database.sqlite') as con:
    countries = pd.read_sql_query("SELECT * from Country", con)
    leagues = pd.read_sql_query("SELECT * from League", con)
    matches = pd.read_sql_query("SELECT * from Match", con)
    players = pd.read_sql_query("SELECT * from Player", con)
    players_attributes = pd.read_sql_query("SELECT * from Player_Attributes", con)
    sqlite_sequences = pd.read_sql_query("SELECT * from sqlite_sequence", con)
    teams = pd.read_sql_query("SELECT * from Team", con)
    team_attributes = pd.read_sql_query("SELECT * from Team_Attributes", con)


Transfers = []
Results = []
for i in range(9,17):
    if(i==9):
        start = '09'
        end = '10'
    else:
        start = str(i)
        end = str(i+1)
    Season = []
    League_List = ['english_premier_league', 'french_ligue_1','german_bundesliga_1','italian_serie_a','spanish_primera_division']
    for league in League_List:
        Season.append(pd.read_csv("data/20" + start + '-' + end + '/' + league+".csv"))
    Transfers.append(Season)
    Standings = []
    League_List = ['Bundesliga', 'EPL','La_Liga','Ligue1','SerieA']
    for league in League_List:
        Standings.append(pd.read_csv("data/Points_table/"+league+"_results/standings_"  + start + end + '_.csv'))
    Results.append(Standings)


Missing_Database_Values_Files = [f for f in listdir("data/European Soccer") if isfile(join("data/European Soccer", f))]
Missing_Database_Values_Files.remove('DataDictionary.xlsx')
Missing_Database_Values = []
for item in Missing_Database_Values_Files:
    Missing_Database_Values.append(pd.read_csv('data/European Soccer/'+item))






'''#EASIER WAY TO MANIPULATE AND FIX DATA.
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3
import matplotlib.pyplot as plt


path = "C:/Users/nar29695/Documents/My created reports/"  #Insert path here
database = path + 'database.sqlite'


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
'''
