# --------------
import pandas as pd 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
# Load the dataset and create column `year` which stores the year in which match was played
df = pd.read_csv(path)
df['Year']= df['date'].apply(lambda x:x[0:4])

# Plot the wins gained by teams across all seasons
d1=df[['match_code','winner']]
d1=d1.drop_duplicates()
d2=d1['winner'].value_counts()
d2.sort_values(ascending=True,inplace=True)
plt.figure(figsize=(10,7))
d2.plot(kind='barh')
plt.xlabel('Matches Won')
plt.ylabel('Teams')
plt.title('IPL Winning teams')
# Plot Number of matches played by each team through all seasons
team_1=df.groupby(['team1'])['match_code'].nunique()
team_2=df.groupby(['team2'])['match_code'].nunique()
matches=team_1+team_2
matches.sort_values(ascending=True,inplace=True)
plt.figure(figsize=(10,7))
matches.plot(kind='barh')
plt.xlabel('Number of matches played')
plt.ylabel('Teams')
plt.title('Total Number of Matches')
# Top bowlers through all seasons
temp=df[['match_code','bowler','wicket_kind']][df['wicket_kind'].notnull()]

nkind=['obstructing the feild','run out','retired hurt']
temp=temp[['match_code','bowler','wicket_kind']][temp['wicket_kind'].isin(nkind) == False]

best_bowler = temp['bowler'].value_counts().idxmax()
print ('Outstanding bowler across seasons is',best_bowler)
wicket_takers=temp['bowler'].value_counts()
#print (wicket_takers)
wicket_takers.head(10).plot(kind='barh')
plt.xlabel('Number of Wickets')
plt.ylabel('Bowler')
plt.title('Wicket taking bowler')
#print (temp['bowler'].value_counts())
#print(temp1)

# How did the different pitches behave? What was the average score for each stadium?
f1=df.groupby(['match_code','inning','venue'])['total'].sum().reset_index()
f2=df.groupby(['venue','inning'])['total'].mean().reset_index()
plt.figure(figsize=(15,7))
plt.plot(f2.loc[f2.inning==1,'venue'],f2.loc[f2.inning==1,'total'],'r',marker='o',label='Inning 1')
plt.plot(f2.loc[f2.inning==2,'venue'],f2.loc[f2.inning==2,'total'],'b',marker='o',label='Inning 2')
plt.legend()
plt.xlabel('Stadium')
plt.xticks(rotation=90)

# Types of Dismissal and how often they occur
d1=df['wicket_kind'].value_counts()
fig,ax=plt.subplots(1,2,figsize=(15,7))
d1.plot(kind='bar',ax=ax[0])
plt.xlabel('Wicket Kind')
plt.ylabel('Number of times')
plt.title('Type of dismissals')
d1.plot(kind='pie',ax=ax[1],autopct='%1.1f%%',explode=[0.02,0,0,0,0,0,0,0,0])
# Plot no. of boundaries across IPL seasons
plt.figure(figsize=(15,7))
run_4=df.loc[df.runs==4,:].reset_index(drop=True)
run_6=df.loc[df.runs==6,:].reset_index(drop=True)
r1=run_4.groupby(['Year'])['runs'].size()
r2=run_6.groupby(['Year'])['runs'].size()
plt.plot(r1.index,r1.values,'r',marker='^',label='Four')
plt.plot(r2.index,r2.values,'b',marker='o',label='Six')
plt.legend()
plt.xlabel('Year')
plt.ylabel('Number of times')
plt.title('Number of boundaries per season')

# Average statistics across all seasons
match_wise_data=df.drop_duplicates(subset='match_code').reset_index(drop=True)
total_runs_scored=df.groupby(['Year'])['total'].sum()
total_ball_bowled=df.groupby(['Year'])['delivery'].count()
match_per_season=match_wise_data.groupby(['Year'])['match_code'].count()
avg_runs_scored_per_match=total_runs_scored/match_per_season
avg_ball_bowled_per_match=total_ball_bowled/match_per_season
avg_runs_each_ball=avg_runs_scored_per_match/avg_ball_bowled_per_match

avg_data=pd.DataFrame([match_per_season,avg_runs_scored_per_match,avg_ball_bowled_per_match,avg_runs_each_ball])
avg_data.index=['Number of Matches','Runs per Match','Deliveries per Match','Runs per Ball']
avg_data=avg_data.T
plt.figure(figsize=(15,7))
avg_data.plot(kind='bar')



