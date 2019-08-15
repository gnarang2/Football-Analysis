
# coding: utf-8

# In[897]:


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
with sqlite3.connect('D:/Football_MyProject/database.sqlite') as con:
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
        x = pd.read_csv("D:/Football_MyProject/Transfers/20" + start + '-' + end + '/' + league+".csv")
        Season.append(x)
    Transfers.append(Season)
    Standings = []
    League_List = ['Bundesliga', 'EPL','La_Liga','Ligue1','SerieA']
    for league in League_List:
        x = pd.read_csv("D:/Football_MyProject/Points_table/"+league+"_results/standings_"  + start + end + '_.csv')
        name = "Standings " + league + " " + start + " "+ end
        x = x.rename(columns={'Unnamed: 0':name})
        Standings.append(x)
    Results.append(Standings)


Missing_Database_Values_Files = [f for f in listdir("D:/Football_MyProject/European Soccer") if isfile(join("D:/Football_MyProject/European Soccer", f))]
Missing_Database_Values_Files.remove('DataDictionary.xlsx')
Missing_Database_Values = []
for item in Missing_Database_Values_Files:
    Missing_Database_Values.append(pd.read_csv('D:/Football_MyProject/European Soccer/'+item))
    


# In[898]:


#Create Dictionaries
teams_dictionary = teams[['team_api_id','team_long_name']].copy()
teams_dictionary = teams_dictionary.set_index('team_api_id')
teams_dictionary = teams_dictionary.to_dict('series')

FIFA_teams_dictionary = teams[['team_fifa_api_id','team_long_name']].copy()
FIFA_teams_dictionary['FIFA_team_long_name'] = FIFA_teams_dictionary['team_long_name']
FIFA_teams_dictionary = FIFA_teams_dictionary[['team_fifa_api_id','FIFA_team_long_name']]
FIFA_teams_dictionary = FIFA_teams_dictionary.set_index('team_fifa_api_id')
FIFA_teams_dictionary = FIFA_teams_dictionary.to_dict('series')

players_dictionary = players[['player_api_id','player_name']].copy()
players_dictionary = players_dictionary.set_index('player_api_id')
players_dictionary = players_dictionary.to_dict('series')

FIFA_players_dictionary = players[['player_fifa_api_id','player_name']].copy()
FIFA_players_dictionary['FIFA_player_name'] = FIFA_players_dictionary['player_name']
FIFA_players_dictionary = FIFA_players_dictionary[['player_fifa_api_id','FIFA_player_name']]
FIFA_players_dictionary = FIFA_players_dictionary.set_index('player_fifa_api_id')
FIFA_players_dictionary = FIFA_players_dictionary.to_dict('series')

leagues_dictionary = leagues[['id','name']].copy()
leagues_dictionary['leagues_name'] = leagues_dictionary['name']
leagues_dictionary = leagues_dictionary[['id','leagues_name']]
leagues_dictionary = leagues_dictionary.set_index('id')
leagues_dictionary = leagues_dictionary.to_dict('series')

countries_dictionary = countries[['id','name']].copy()
countries_dictionary['countries_name'] = countries_dictionary['name']
countries_dictionary = countries_dictionary[['id','countries_name']]
countries_dictionary = countries_dictionary.set_index('id')
countries_dictionary = countries_dictionary.to_dict('series')

positions_dictionary = Missing_Database_Values[5].copy()
positions_dictionary = positions_dictionary[['player_pos_x','player_pos_y','role_xy']]
positions_dictionary = positions_dictionary.astype(str)
positions_dictionary['pos'] = positions_dictionary['player_pos_x']+positions_dictionary['player_pos_y']
positions_dictionary = positions_dictionary[['pos','role_xy']]
positions_dictionary['pos'] = positions_dictionary['pos'].astype(int)
positions_dictionary = positions_dictionary.set_index('pos')
positions_dictionary = positions_dictionary.to_dict('series')


#Create Dictionary for having Goals, basically combining all information together. Check Data_Dictionary in European Soccer for more information
Goals = Missing_Database_Values[4][['id','match_id', 'team', 'elapsed','elapsed_plus','player1','player2','goal_type','subtype']].copy().fillna(0)
Goals[['id','match_id','team','elapsed','elapsed_plus','player1','player2']] = Goals[['id','match_id','team','elapsed','elapsed_plus','player1','player2']].astype(int)
Goals['match_id'] = Goals['match_id'].astype(str)
Goals['Combined_Goals'] = list(zip(Goals.team,Goals.elapsed, Goals.elapsed_plus,Goals.player1,Goals.player2,Goals.goal_type,Goals.subtype))
goals_dictionary = Goals[['id','Combined_Goals']].copy()
goals_dictionary = goals_dictionary.rename(columns={'Combined_Goals':'goals'})
goals_dictionary = goals_dictionary.set_index('id')
goals_dictionary = goals_dictionary.to_dict('series')

#Creating a key for the goals containing information regarding goals scored keys
goals_dictionary_key = Goals[['id','match_id']].copy()
goals_dictionary_key = goals_dictionary_key.rename(columns={'id':'goals_id'})
goals_dictionary_key = goals_dictionary_key.groupby('match_id')['goals_id'].apply(list)
goals_dictionary_key = goals_dictionary_key.reset_index()
goals_dictionary_key['match_id'] = goals_dictionary_key['match_id'].astype(int)
goals_dictionary_key = goals_dictionary_key.set_index('match_id')
goals_dictionary_key = goals_dictionary_key.to_dict('series')

#Creating a combined dictionary for apply functions
all_dictionary_key = {"goals":"goals","goals_id":"goals_id","position":"role_xy","countries":"countries_name","teams":"team_long_name","FIFA_teams":"FIFA_team_long_name","leagues":"leagues_name","players":"player_name","FIFA_players":"FIFA_player_name"}
all_dictionary = {**goals_dictionary,**goals_dictionary_key,**positions_dictionary,**countries_dictionary,**teams_dictionary,**FIFA_teams_dictionary,**players_dictionary,**FIFA_players_dictionary,**leagues_dictionary}
return_dictionary = {"goals":tuple(),"goals_id":[],"position":"","countries":"","teams":"","FIFA_teams":"","leagues":"","players":"","FIFA_players":""}
#Function to get names of all types of IDs
def get_name(ID,ID_type):
    if(all_dictionary_key.get(ID_type,"None")=="None"):
        return None
    key = all_dictionary_key[ID_type]
    if(all_dictionary[key].get(ID,"None")=="None"):
        return return_dictionary[ID_type]
    return all_dictionary[key][ID]
#Teams in top five leagues
Relevant_IDs = [1729,4769,7809,10257,21518]
#Teams not in top five leagues
Irrelevant_IDs = [1, 13274, 15722, 17642, 19694, 24558]




# In[899]:


#Removing teams not in top five leagues, season 2008/09 and also sorting NA values for player names.
for ID in Irrelevant_IDs:
    indexNames = matches[matches['league_id'] == ID].index
    matches = matches.drop(indexNames)
matches = matches[matches['season']!='2008/2009']
matches = matches.dropna(subset=['away_player_X11', 'away_player_Y11'])

#Finding position of players, linking it from the IDs and the relevant dictionary
for col in list(matches.columns)[11:55]:
    matches[col] = matches[col].astype(int)
    matches[col] = matches[col].astype(str)
for col in list(matches.columns)[11:33]:
    col11 = col[:12]+'Y'+col[13:]
    matches[col] = matches[col]+matches[col11]
    matches[col] = matches[col].astype(int)
    matches = matches.replace({col:positions_dictionary["role_xy"]})
    matches = matches.replace({col11:positions_dictionary["role_xy"]})
    matches = matches.drop([col11] ,  axis='columns')
matches['goal'] = matches['id'].apply(lambda x: get_name(x,'goals_id'))

#Expanding match['goal'] to have multiple columns for better sorting.
goals_expand = matches['goal'].copy()
goals_expand = pd.DataFrame(goals_expand)
goals_expand = goals_expand.reset_index()
goals_expand = pd.DataFrame(goals_expand['goal'].tolist(), columns=['Goal1','Goal2','Goal3','Goal4','Goal5','Goal6','Goal7','Goal8','Goal9','Goal10','Goal11','Goal12'])
goals_expand['match_id'] = matches.index.copy()

#Joining goals_expand into match['goal']
matches = matches.merge(goals_expand, left_on='id', right_on='match_id')
matches = matches.drop(columns=['match_id'])


# In[905]:


#Create only one plot for each, later we will convert it into loops.
#Season Plots
#Team Plots
#PLayer Plots


# In[922]:


#Create dictionaries for every fkn thing along with relevant function


# Season Analysis: Do for each league separately and then combined too. 
# 1. Get column for last five and last three and last game(s) results for both home and away team
# 2. Home team winning at what stages of the season
# 3. Impact on goals scored / points / position based on transfers in / out as well as transfer money spent
# 4. Shots on / off target accuracy including whether the led to the goal
# 5. Goal types - penalty....
# 6. Fouls commited / Cards leading to anything on goals/points/victory
# 7. Do crosses / corners  impact goals scored 
# 8. Go into possession stats checking what grouping of possession 10-20,20-30,90-100 led to maximum victories
# Basically we need to answer what leads to more goals and more points.
# 9. how many times team scoring first won? Both home and away separately. 
# 10. how does position impact a player from scoring.
# 11. 

# Overall Analysis:
# 1. Position in league based on previous league position
# 2. Home team winnin at what stages of the season
# 3. Impact on goals scored / points / position based on transfers in / out as well as transfer money spent
# 4. 

# TO DO:
# 
# First Data Analysis Technique we will use is regression:
# 1. Ridge Regression
# 2. Stepwise Regression
# 
# Potential Target Variables for Regression: Goals scored by a team in a match, Points / Wins of a team in a season
# 
# Variables for Goals scored by a team in a match: 
# 1. General Level: Results from last 1/3/5 games, Home / Away, Posession, Cards, Shots, Fouls, Crosses, Corners, Current position of the team and the opponent in the league before the match, stage of the season
# 2. Deeper Level: Number of top level goal scorers from the last season, goals scored in previous 1/3/5 matches, scorer(s) from previous game in line up, how early the team's first goal was, goals to games ratio so far, did they score the first goal, number of forwards in the team, number of midfielders in the team, number of defenders in the team, 

# In[914]:


df = pd.DataFrame()


# In[915]:


df['x'] = ['A','A','C','D']
df['y'] = [1,2,3,4]


# In[916]:


df


# In[917]:


df = df.groupby('x')


# In[921]:


for key, item in df:
    print(item)

