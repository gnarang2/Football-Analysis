
# coding: utf-8

# In[134]:


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
        x = pd.read_csv("data/20" + start + '-' + end + '/' + league+".csv")
        Season.append(x)
    Transfers.append(Season)
    Standings = []
    League_List = ['Bundesliga', 'EPL','La_Liga','Ligue1','SerieA']
    for league in League_List:
        x = pd.read_csv("data/Points_table/"+league+"_results/standings_"  + start + end + '_.csv')
        name = "Standings " + league + " " + start + " "+ end
        x = x.rename(columns={'Unnamed: 0':name})
        Standings.append(x)
    Results.append(Standings)


Missing_Database_Values_Files = [f for f in listdir("data/European Soccer") if isfile(join("data/European Soccer", f))]
Missing_Database_Values_Files.remove('DataDictionary.xlsx')
Missing_Database_Values = []
for item in Missing_Database_Values_Files:
    Missing_Database_Values.append(pd.read_csv('data/European Soccer/'+item))






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

positions_dictionary = Missing_Database_Values[7].copy()
positions_dictionary = positions_dictionary[['player_pos_x','player_pos_y','role_xy']]
positions_dictionary = positions_dictionary.astype(str)
positions_dictionary['pos'] = positions_dictionary['player_pos_x']+positions_dictionary['player_pos_y']
positions_dictionary = positions_dictionary[['pos','role_xy']]
positions_dictionary['pos'] = positions_dictionary['pos'].astype(int)
positions_dictionary = positions_dictionary.set_index('pos')
positions_dictionary = positions_dictionary.to_dict('series')


#Create Dictionary for having Goals, basically combining all information together. Check Data_Dictionary in European Soccer for more information
Goals = Missing_Database_Values[4][['id','match_id', 'team', 'elapsed','elapsed_plus','player1','goal_type','subtype']].copy().fillna(0)
Goals[['id','match_id','team','elapsed','elapsed_plus','player1']] = Goals[['id','match_id','team','elapsed','elapsed_plus','player1']].astype(int)
Goals['match_id'] = Goals['match_id'].astype(str)
Goals['Combined_Goals'] = list(zip(Goals.team,Goals.elapsed, Goals.elapsed_plus,Goals.player1,Goals.goal_type,Goals.subtype))
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

# print(goals_expand['goal'].tolist())
goals_expand = pd.DataFrame(goals_expand['goal'].tolist())
goals_expand['match_id'] = matches.index.copy()

#Joining goals_expand into match['goal']
matches = matches.merge(goals_expand, left_on='id', right_on='match_id')
matches = matches.drop(columns=['match_id'])

goals_dictionary_key = Goals[['id','match_id']].copy()
goals_dictionary_key = goals_dictionary_key.rename(columns={'id':'goals_id'})
goals_dictionary_key = goals_dictionary_key.groupby('match_id')['goals_id'].apply(list)
goals_dictionary_key = goals_dictionary_key.reset_index()
goals_dictionary_key['match_id'] = goals_dictionary_key['match_id'].astype(int)

all_dictionary_key['home_opponent'] = 'home_opponent'
all_dictionary_key['away_opponent']='away_opponent'

away_teams_opponents = matches[['id','home_team_api_id']].copy()
away_teams_opponents = away_teams_opponents.rename(columns={'home_team_api_id':'home_opponent'})
away_teams_opponents = away_teams_opponents.set_index('id')
away_teams_opponents = away_teams_opponents.to_dict('series')

home_teams_opponents = matches[['id','away_team_api_id']].copy()
home_teams_opponents = home_teams_opponents.rename(columns={'away_team_api_id':'away_opponent'})
home_teams_opponents = home_teams_opponents.set_index('id')
home_teams_opponents = home_teams_opponents.to_dict('series')

all_dictionary['away_opponent'] =home_teams_opponents['away_opponent']
all_dictionary['home_opponent'] =away_teams_opponents['home_opponent']






# In[497]:


matches


# In[509]:


goals_dictionary


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

# In[502]:


Regression_Data = matches[['id', 'country_id', 'league_id', 'season', 'stage', 'date', 'match_api_id','home_team_api_id',
 'away_team_api_id']].copy()
Regression_Data = Regression_Data.melt(id_vars=['id', 'country_id', 'league_id', 'season', 'stage', 'date', 'match_api_id'],
        var_name="Home_or_Away", value_name="Team_id")
#df.loc[(df['Club']==League),'League'] = 'Bundesliga'
Regression_Data.loc[(Regression_Data['Home_or_Away']=='home_team_api_id'),'Home_or_Away'] = 'Home'
Regression_Data.loc[(Regression_Data['Home_or_Away']=='away_team_api_id'),'Home_or_Away'] = 'Away'
Regression_Data['Opponent_id'] = Regression_Data['id']
Regression_Data['Points Gained'] = 0
#Regression_Data.loc[(Regression_Data['Home_or_Away']=='Home'),'Opponent_id'] = '1'
Regression_Data['Opponent_id'] = Regression_Data.apply(lambda x: get_name(x['id'],'away_opponent') if x['Home_or_Away'] == "Home" else get_name(x['id'],'home_opponent'),axis=1 )
def points(x):
    if(x['Home_or_Away'] == "Home"):
        if (x["home_team_goal"] > x["away_team_goal"]):
            return 3
        if (x["home_team_goal"] < x["away_team_goal"]):
            return 0
    if(x['Home_or_Away'] == "Away"):
        if (x["home_team_goal"] > x["away_team_goal"]):
            return 0
        if (x["home_team_goal"] < x["away_team_goal"]):
            return 3
    return 1
Regression_Data = pd.merge(Regression_Data, matches[['id','home_team_goal', 'away_team_goal', 'home_player_X1', 'home_player_X2',
 'home_player_X3', 'home_player_X4', 'home_player_X5', 'home_player_X6', 'home_player_X7',
 'home_player_X8', 'home_player_X9', 'home_player_X10', 'home_player_X11', 'away_player_X1',
 'away_player_X2', 'away_player_X3', 'away_player_X4', 'away_player_X5', 'away_player_X6',
 'away_player_X7', 'away_player_X8', 'away_player_X9', 'away_player_X10', 'away_player_X11',
 'home_player_1', 'home_player_2', 'home_player_3', 'home_player_4', 'home_player_5', 'home_player_6',
 'home_player_7', 'home_player_8', 'home_player_9', 'home_player_10', 'home_player_11', 'away_player_1',
 'away_player_2', 'away_player_3', 'away_player_4', 'away_player_5', 'away_player_6', 'away_player_7',
 'away_player_8', 'away_player_9', 'away_player_10', 'away_player_11', 'goal', 'shoton', 'shotoff',
 'foulcommit', 'card', 'cross', 'corner', 'possession', 'B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA',
 'IWH', 'IWD', 'IWA', 'LBH', 'LBD', 'LBA', 'PSH', 'PSD', 'PSA', 'WHH', 'WHD', 'WHA', 'SJH', 'SJD',
 'SJA', 'VCH', 'VCD', 'VCA', 'GBH', 'GBD', 'GBA', 'BSH', 'BSD', 'BSA']], on='id')

Regression_Data['Points Gained'] = Regression_Data.apply(lambda x: points(x),axis=1)
#Regression_Data['']


Regression_Data['date'] =pd.to_datetime(Regression_Data.date)

def results(x,number):
    tup = (x['season'],x['Team_id'])
    idx = x['index']
    if number == 1: return Last_Result[tup][idx]
    if number == 3: return Last_Three_Results[tup][idx]
    if number == 5: return Last_Five_Results[tup][idx]

Last_Five_Results = {}
Last_Three_Results = {}
Last_Result = {}
m = Regression_Data.copy().groupby(['season','Team_id'])
for key, item in m:
    #sort by date first.
    item= item.sort_values(by="stage")
    Last_Result[key] = item['Points Gained'].shift(1)
    Last_Three_Results[key] = Last_Result[key]+item['Points Gained'].shift(2)+item['Points Gained'].shift(3)
    Last_Five_Results[key] = Last_Three_Results[key]+item['Points Gained'].shift(4)+item['Points Gained'].shift(5)


Regression_Data = Regression_Data.reset_index()
Regression_Data['Last_Five_Results'] = Regression_Data.apply(lambda x: results(x,5),axis=1)
Regression_Data['Last_Three_Results'] = Regression_Data.apply(lambda x: results(x,3),axis=1)
Regression_Data['Last_Result'] = Regression_Data.apply(lambda x: results(x,1),axis=1)
Regression_Data['Goals_Conceded'] = Regression_Data.apply(lambda x: x['home_team_goal'] if x['Home_or_Away'] == 'Away' else x['away_team_goal'],axis=1)
Regression_Data['Goals_Scored'] = Regression_Data.apply(lambda x: x['home_team_goal'] if x['Home_or_Away'] == 'Home' else x['away_team_goal'],axis=1)
Regression_Data['Goal_Difference'] = Regression_Data['Goals_Scored']-Regression_Data['Goals_Conceded']

Regression_Data['Goal_Difference'] = Regression_Data.sort_values(by=["season","stage"]).groupby(['season','Team_id']).Goal_Difference.cumsum()
Regression_Data['Total_Points'] = Regression_Data.sort_values(by=["season","stage"]).groupby(['season','Team_id'])['Points Gained'].cumsum()

m = Regression_Data[['season','stage','league_id','id','Total_Points','Team_id']].copy().sort_values(by=["season","stage"]).groupby(['season','stage', 'league_id'])
Position = {}
for key, item in m:
    #sort by date first.
    item = item.sort_values(by="Total_Points")
    item['Rank'] = item['Total_Points'].rank(ascending = 0,method='first')
    item = item.sort_values(by="Rank")
    Position[key] = item

def pos(x,team):
    item = Position[(x['season'],x['stage'],x['league_id'])]
    if(team=="Own"):
        item = item[item['Team_id']==x['Team_id']]['Rank']
    else:
        item = item[item['Team_id']==x['Opponent_id']]['Rank']
    index = item.index
    return item[index[0]].astype(int)

Regression_Data['League_Position_Own'] = Regression_Data.apply(lambda x: pos(x,"Own"),axis=1)
Regression_Data['League_Position_Opp'] = Regression_Data.apply(lambda x: pos(x,"Opponent"),axis=1)

Regression_Data = Regression_Data.merge(goals_expand, left_on='id', right_on='match_id').drop(columns=['match_id'])


# In[209]:


#Posession, Cards, Shots, Fouls, Crosses, Corners,


# In[503]:


m = Regression_Data.merge(goals_expand, left_on='id', right_on='match_id').drop(columns=['match_id']).copy()


# In[504]:


m


# In[507]:


d = goals_expand.set_index('match_id').copy()


# In[514]:


d = d.fillna(0).astype(int)
for i in d.columns:
    d[i] = d[i].apply(lambda x: get_name(x,"goals"))


# In[515]:


d
