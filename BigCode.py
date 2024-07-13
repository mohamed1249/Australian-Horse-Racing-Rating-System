import pandas as pd
from datetime import  datetime
from datetime import date, timedelta
import json
from urllib.request import urlopen
import requests
import time
import glob
import os
from pandas.errors import EmptyDataError
import warnings
warnings.filterwarnings('ignore')
import numpy as np
np.random.seed(31415)
import tensorflow as tf
tf.random.set_seed(31415)
os.environ['PYTHONHASHSEED'] = str(31415)
os.environ['TF_DETERMINISTIC_OPS'] = '1'
import pickle as pk

for root, _, files in os.walk('NewData'):
        for file in files:
            if file.endswith('.csv') or file.endswith('.xlsx'):
                os.remove(os.path.join(root, file))
                print(f'{os.path.join(root, file)} Deleted!')

today = date.today()
rundate = today + timedelta(days=0)
dte = rundate.strftime('%d-%m-%Y')
etd = rundate.strftime('%Y-%m-%d')
date1 = etd
date = dte
fldr = etd

api = '?ApiKey='

jkyurl = "https://www.puntingform.com.au/api/formdataservice/GetJockeyStrikeRateData/"

trnurl = "https://www.puntingform.com.au/api/formdataservice/GetTrainerStrikeRateData/"

jky = 'Jockeys SR'
JkySR = jkyurl+dte+api

trn = 'Trainers SR'
TrnSR = trnurl+dte+api

jkysr = pd.read_csv(JkySR, index_col=False)
jkysr = jkysr.sort_values(by=['L100ExpWins'], ascending=False)
jkysr.to_csv(f"./NewData/JockeySR/{etd} - %s.csv"%jky, index=False)

trnsr = pd.read_csv(TrnSR, index_col=False)
trnsr = trnsr.sort_values(by=['L100Wins'], ascending=False)
trnsr.to_csv(f"./NewData/TrainerSR/{etd} - %s.csv"%trn, index=False)

mtgsurl = 'https://www.puntingform.com.au/api/formdataservice/GetMeetings/'
ratingsurl = "https://www.puntingform.com.au/api/ratingsservice/GetRatingsText"

mtgs_url = (mtgsurl + date + api)
response = urlopen(mtgs_url)

data_json = json.loads(response.read())
df = pd.DataFrame(data_json)

track_names = df['Value']
fns = track_names.tolist()

track = df['Value'].str.replace(' ', '%20')
track_list = track.tolist()
team = track_list

for t in team:
    f"{ratingsurl}/{t}/{date}{api}"

ratingsurl = [f'{ratingsurl}/{t}/{date}{api}' for t in team]

inputs = zip(ratingsurl, fns)

def download_url(args):
    ratingsurl, fn = args[0], args[1]
    try:
        r = requests.get(ratingsurl)
        with open(f'./NewData/MeetingFiles/%s-{fn}-Ratings.csv'%date1, 'wb') as f:
            f.write(r.content)
        return(ratingsurl, time.time())
    except Exception as e:
        print('Exception in download_url():', e)

t0 = time.time()
for i in inputs:
    result = download_url(i)

path = f'./NewData/MeetingFiles/'

all_files = glob.glob(path + date1+'*-Ratings.csv')

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=False, header=0)
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=False)

df.drop(['PdfPath', 'PublishTime'], axis=1, inplace=True)
df.rename(columns={'ClsDiff': 'Class Change', 'RunStyle': 'Historical Run Style', 'PrSe': 'Predicted Settling Position', 'PFScore': 'PF Score 0-100', 'AHSP': 'Average Historical Settling Pos %', 'RPP': 'Neural Price', 'RPR': 'Neural Rank', 'ScRank': 'Last 600m Ranking Late Speed', 'WP20R': 'Weight Class Rank', 'TP20R': 'Time Ranking Start to Finish', 'WPTP20R': 'Time Adjust - Weight/Class Rank', 'ETRPrRk': 'Early Time Ranking to 600m Speed'}, inplace=True)

df.replace([900,25], '-', inplace=True)

df.to_csv('./NewData/Ratings/%s - RatingsSheet.csv' %date1, index=False)

Fieldsurl = 'https://www.puntingform.com.au/api/formdataservice/GetFields'

for t in team:
    f"{Fieldsurl}/{t}/{dte}{api}"

Fieldsurl = [f'{Fieldsurl}/{t}/{dte}{api}' for t in team]

inputs = zip(Fieldsurl, fns)

def download_url(args):
    Fieldsurl, fn = args[0], args[1]
    try:
        r = requests.get(Fieldsurl)
        with open(f'./NewData/Fields/MeetingFields/{etd}-{fn} - Field.csv', 'wb') as f:
            f.write(r.content)
        return(Fieldsurl, time.time())
    except Exception as e:
        print('Exception in download_url():', e)

t0 = time.time()
for i in inputs:
    result = download_url(i)




path = f'./NewData/Fields/MeetingFields/' # use your pathC:\Users\bjj07\OneDrive\2. VSCFiles\3_Horse Racing\Testing\In Work\GetFormText
all_files = glob.glob(path + f"/{etd}*.csv")

li = []
bad_files = []

for filename in all_files:
    try:
        df = pd.read_csv(filename, index_col=False, header=0)
        li.append(df)

    except EmptyDataError:
        print(f'No columns to parse from file {filename}')
        bad_files.append(filename)


df = pd.concat(li, axis=0, ignore_index=False)

results = etd + ' - Fields'

df.to_csv('./NewData/Fields/%s.csv' %results)

Formurl = 'https://www.puntingform.com.au/api/formdataservice/GetExtendedFormText'

raceno = [*range(1,13,1)]

Formurls = [f'{Formurl}/{t}/{r}/{dte}{api}' for t in team for r in raceno]

fns = [f'./NewData/Form/TempFiles/Form-{t}-R{r}.csv' for t in team for r in raceno]

inputs = zip(Formurls, fns)

def download_url(args):
    t0 = time.time()
    Formurl, fn = args[0], args[1]
    try:
        r = requests.get(Formurl)
        with open(fn, 'wb') as f:
            f.write(r.content)
        return(Formurl, time.time() - t0)
    except Exception as e:
        print('Exception in download_url():', e)

t0 = time.time()
for i in inputs:
    result = download_url(i)
    print('url:', result[0], 'time:', result[1])
print('Total time:', time.time() - t0)

results = etd +'-'+ 'All Meetings'

path = f'./NewData/Form/TempFiles' # use your pathC:\Users\bjj07\OneDrive\2. VSCFiles\3_Horse Racing\Testing\In Work\GetFormText
all_files = glob.glob(path + "/Form*.csv")

li = []
bad_files = []

for filename in all_files:
    try:
        df = pd.read_csv(filename, index_col=False, header=0)
        li.append(df)

    except EmptyDataError:
        print(f'No columns to parse from file {filename}')
        bad_files.append(filename)


df2 = pd.concat(li, axis=0, ignore_index=False)

df2.to_csv('./NewData/Form/%s.csv' %results, index=False)
df2.to_excel('./NewData/Form/ExcelFiles/%s.xlsx' %results, index=False)


time.sleep(5)

files = glob.glob('./NewData/Form/TempFiles/*')
for f in files:
    os.remove(f)



today = date.today()

today = date.today()

currdate2 = today.strftime('%y-%m-%d')
rating = "https://betfair-data-supplier-prod.herokuapp.com/api/widgets/kash-ratings-model/datasets?date=20"+currdate2+"&presenter=RatingsPresenter&csv=true"
Kash=pd.read_csv(rating)
currdate1 = today.strftime('%d/%m/%Y')
Kash["Date"]=currdate1
Kash["meetings.name"]=Kash["meetings.name"].str.title()
print(Kash)

Kash.to_csv('NewData/CarrotCruncherModelUpdate.csv',mode='a',index=False)
currdate = datetime.strptime(currdate2,'%y-%m-%d')
currdate += timedelta(days=1)
df = pd.DataFrame(Kash)

df.to_csv(f'NewData/{today}-CarrotCrusher.csv')


btdays = 0

today = date.today()
rundate = today - timedelta(days=btdays)
dte = rundate.strftime('%d-%m-%Y')
etd = rundate.strftime('%Y-%m-%d')

formdate = rundate.strftime("%Y%m%d")
track = 'All Meetings'
meeting = etd+'-'+track

form_df = pd.read_csv('./NewData/Form/%s.csv'%meeting)

for col in form_df.columns:
  print(col)

form_cols = ['meeting date', 'horse sire', 'horse dam', 'horse prize money', 'horse record synthetic', ' form trainer id', ' form jockey id', 'prizemoney', 'prizemoney won', 'country', 'race prizemoney', 'race name', 'jockeys can claim']
form_df.drop(columns=form_cols, inplace=True)

x = 2
form_df1 = form_df.groupby(['horse name', 'track', 'race number']).head(x)


form_df2 = form_df1.drop_duplicates(subset=['horse name', 'track', 'race number'], keep='first')


form_df3 = form_df1.drop_duplicates(subset=['horse name', 'track', 'race number'], keep='last')

form_df3 = form_df3[['race number', 'horse number', 'horse name', 'form barrier', 'form class', 'form distance', 'form jockey', 'form margin', 'form meeting date', 'form other runners', 'form position', 'form price', 'form track', 'form track condition', 'form weight']]

form_df3['form meeting date'] =  pd.to_datetime(form_df3['form meeting date'])
form_df3['form meeting date'] = form_df3['form meeting date'].dt.strftime('%d-%m-%Y')
form_df3['form meeting date'] =form_df3['form meeting date'].apply(pd.to_datetime)
form_df3['DLR-2'] = (pd.to_datetime('today') - form_df3['form meeting date']).dt.days - btdays

form_df3.rename(columns={'horse name':'Horse', 'race number':'Race Number', 'horse number':'Tab Number', 'form position':'Form Pos-2', 'form margin':'Form Margin-2', 'form price':'Form Price-2', 'form barrier':'Form Barrier-2', 'form class':'Form Class-2', 'form distance':'Form Dist-2', 'form jockey':'Form Jky-2', 'form margin':'Form Margin-2',  'form price':'Form Price-2', 'form track':'Form Track-2', 'form track condition':'Form Tr Cond-2', 'form weight':'Form Weight-2', 'form meeting date':'Form Mtg Date-2', 'form other runners':'Form Other Runners-2'}, inplace=True)

form_df3.to_csv('NewData/2nd Last Run-Form.csv', index=False)

x = 3
form_df4 = form_df.groupby(['horse name', 'track', 'race number']).head(x)
form_df5 = form_df4.drop_duplicates(subset=['horse name', 'track', 'race number'], keep='last')


form_df5.drop(form_df5.loc[form_df5['track']=='track'].index, inplace=True)
form_df6 = form_df5[['race number', 'horse number', 'horse name', 'form barrier', 'form class', 'form distance', 'form jockey', 'form margin', 'form meeting date', 'form other runners', 'form position', 'form price', 'form track', 'form track condition', 'form weight']]
form_df6.rename(columns={'horse name':'Horse', 'race number':'Race Number', 'horse number':'Tab Number', 'form position':'Form Pos-3', 'form margin':'Form Margin-3', 'form price':'Form Price-3', 'form barrier':'Form Barrier-3', 'form class':'Form Class-3', 'form distance':'Form Dist-3', 'form jockey':'Form Jky-3', 'form margin':'Form Margin-3',  'form price':'Form Price-3', 'form track':'Form Track-3', 'form track condition':'Form Tr Cond-3', 'form weight':'Form Weight-3', 'form meeting date':'Form Mtg Date-3', 'form other runners':'Form Other Runners-3'}, inplace=True)

form_df6['Form Mtg Date-3'] =  pd.to_datetime(form_df6['Form Mtg Date-3'])
form_df6['Form Mtg Date-3'] = form_df6['Form Mtg Date-3'].dt.strftime('%d-%m-%Y')
form_df6['Form Mtg Date-3'] =form_df6['Form Mtg Date-3'].apply(pd.to_datetime)
form_df6['DLR-3'] = (pd.to_datetime('today') - form_df6['Form Mtg Date-3']).dt.days - btdays

form_df6.to_csv('NewData/3nd Last Run-Form.csv', index=False)

form_df2[["Minutes", "Secs"]] = form_df2["form time"].str.split(pat=":", expand=True)
form_df2[["Seconds", "MSecs"]] = form_df2["Secs"].str.split(pat=".", expand=True)
form_df2["Minutes"] = form_df2["Minutes"].astype(int)
form_df2["Seconds"] = form_df2["Seconds"].astype(int)
form_df2["MSecs"] = form_df2["MSecs"].astype(int)
form_df2['Minutes'] = form_df2["Minutes"].apply(lambda x: x*60)
form_df2['MSecs'] = form_df2["MSecs"].apply(lambda x: x/100)
form_df2['Time'] = form_df2["Minutes"] + form_df2["Seconds"]
form_df2['RunTime'] = form_df2["Time"] + form_df2["MSecs"]

form_df2.rename(columns={'horse last10':'horselast10'}, inplace=True)

def inrun(row):
    if row['form position'] == 1:
        val = 0
    elif row['form position'] > 1:
        val = row['form margin']
    else:
        val = 0
    return val
form_df2['margin'] = form_df2.apply(inrun, axis=1)

form_df2["margin"] = form_df2["margin"].astype(float)
form_df2['MarginTime'] = form_df2["margin"].apply(lambda x: x*0.2)
form_df2['RunnerTime'] = form_df2["RunTime"] + form_df2["MarginTime"]

form_df2[["Race Starts", "Race Wins"]] = form_df2["horse record"].str.split(pat=":", expand=True)
form_df2[["Race Wins", "RDrop", "RDrop1"]] = form_df2["Race Wins"].str.split(pat="-", expand=True)

form_df2[["Dist Starts", "Dist Wins"]] = form_df2["horse record distance"].str.split(pat=":", expand=True)
form_df2[["Dist Wins", "DDrop", "DDrop1"]] = form_df2["Dist Wins"].str.split(pat="-", expand=True)

form_df2[["Track Starts", "Track Wins"]] = form_df2["horse record track"].str.split(pat=":", expand=True)
form_df2[["Track Wins", "TDrop", "TDrop1"]] = form_df2["Track Wins"].str.split(pat="-", expand=True)

form_df2[["Tr-Dist Starts", "Tr-Dist Wins"]] = form_df2["horse record track distance"].str.split(pat=":", expand=True)
form_df2[["Tr-Dist Wins", "TDDrop", "TDDrop1"]] = form_df2["Tr-Dist Wins"].str.split(pat="-", expand=True)

form_df2[["Good Starts", "Good Wins"]] = form_df2["horse record good"].str.split(pat=":", expand=True)
form_df2[["Good Wins", "GDrop", "GDrop1"]] = form_df2["Good Wins"].str.split(pat="-", expand=True)
form_df2[["Soft Starts", "Soft Wins"]] = form_df2["horse record soft"].str.split(pat=":", expand=True)
form_df2[["Soft Wins", "SDrop", "SDrop1"]] = form_df2["Soft Wins"].str.split(pat="-", expand=True)
form_df2[["Heavy Starts", "Heavy Wins"]] = form_df2["horse record heavy"].str.split(pat=":", expand=True)
form_df2[["Heavy Wins", "HDrop", "HDrop1"]] = form_df2["Heavy Wins"].str.split(pat="-", expand=True)

form_df2[["1st Up Starts", "1st Up Wins"]] = form_df2["horse record first up"].str.split(pat=":", expand=True)
form_df2[["1st Up Wins", "1Drop", "1Drop1"]] = form_df2["1st Up Wins"].str.split(pat="-", expand=True)

form_df2[["2nd Up Starts", "2nd Up Wins"]] = form_df2["horse record second up"].str.split(pat=":", expand=True)
form_df2[["2nd Up Wins", "2Drop", "2Drop1"]] = form_df2["2nd Up Wins"].str.split(pat="-", expand=True)

columns = ['1Drop','1Drop1', "GDrop", "GDrop1", "SDrop", "SDrop1", "HDrop", "HDrop1", "RDrop", "RDrop1", "DDrop", "DDrop1", "TDrop", "TDrop1", "TDDrop", "TDDrop1", "2Drop", "2Drop1"]
form_df2[columns] = form_df2[columns].astype(float)

form_df2['1st Up Placings'] = form_df2.loc[:,['1Drop','1Drop1']].sum(axis=1)
form_df2['2nd Up Placings'] = form_df2.loc[:,['2Drop','2Drop1']].sum(axis=1)
form_df2['Race Placings'] = form_df2.loc[:,['RDrop','RDrop1']].sum(axis=1)
form_df2['Dist Placings'] = form_df2.loc[:,['DDrop','DDrop1']].sum(axis=1)
form_df2['Track Placings'] = form_df2.loc[:,['TDrop','TDrop1']].sum(axis=1)
form_df2['Tr-Dist Placings'] = form_df2.loc[:,['TDDrop','TDDrop1']].sum(axis=1)
form_df2['Good Placings'] = form_df2.loc[:,['GDrop','GDrop1']].sum(axis=1)
form_df2['Soft Placings'] = form_df2.loc[:,['SDrop','SDrop1']].sum(axis=1)
form_df2['Heavy Placings'] = form_df2.loc[:,['HDrop','HDrop1']].sum(axis=1)

form_df2["horselast10"] = form_df2["horselast10"].convert_dtypes()
form_df2["horselast10"].dtype

form_df2['RFS'] = form_df2['horselast10'].str.split('x').str[-1]

form_df2['RFS_Count'] = form_df2['RFS'].str.count(r'\d')

form_df2[["Date", "Time"]] = form_df2["start time"].str.split(pat=" ", expand=True)

form_df2[["Last 600m", "SsDrop"]] = form_df2["sectional"].str.split(pat="s", expand=True)

form_df2.drop(['RDrop', 'RDrop1', 'DDrop', 'DDrop1', 'TDrop', 'TDrop1', 'TDDrop', 'TDDrop1', 'start time', "GDrop", "GDrop1", "SDrop", "SDrop1", "HDrop", "HDrop1", "1Drop", "1Drop1", "2Drop", "2Drop1", 'Minutes', 'Secs', 'Seconds',	'MSecs', 'RunTime', 'margin', 'MarginTime', 'SsDrop', 'sectional'], axis = 1, inplace = True)

columns = ['Race Wins', 'Race Starts', 'Dist Wins', 'Dist Starts', 'Track Wins', 'Track Starts', 'Tr-Dist Wins', 'Tr-Dist Starts' , 'Good Wins', 'Good Starts', 'Soft Wins','Soft Starts', 'Heavy Wins', 'Heavy Starts', "1st Up Starts", "1st Up Wins" , "2nd Up Starts", "2nd Up Wins", 'RFS_Count']
form_df2[columns] = form_df2[columns].astype(float)

form_df2['Dist SR'] = form_df2['Dist Wins']/form_df2['Dist Starts'] * 100
form_df2['Win SR'] = form_df2['Race Wins']/form_df2['Race Starts'] * 100
form_df2['Track SR'] = form_df2['Track Wins']/form_df2['Track Starts'] * 100
form_df2['Tr-Dist SR'] = form_df2['Tr-Dist Wins']/form_df2['Tr-Dist Starts'] * 100
form_df2['Good SR'] = form_df2['Good Wins']/form_df2['Good Starts'] * 100
form_df2['Soft SR'] = form_df2['Soft Wins']/form_df2['Soft Starts'] * 100
form_df2['Heavy SR'] = form_df2['Heavy Wins']/form_df2['Heavy Starts'] * 100
form_df2['1st Up SR'] = form_df2['1st Up Wins']/form_df2['1st Up Starts'] * 100
form_df2['2nd Up SR'] = form_df2['2nd Up Wins']/form_df2['2nd Up Starts'] * 100

form_df2 = form_df2.round(2)

form_df2['form meeting date'] =  pd.to_datetime(form_df2['form meeting date'])
form_df2['form meeting date'] = form_df2['form meeting date'].dt.strftime('%d-%m-%Y')
form_df2['form meeting date'] =form_df2['form meeting date'].apply(pd.to_datetime)
form_df2['DLR-1'] = (pd.to_datetime('today') - form_df2['form meeting date']).dt.days - btdays

form_df2.to_csv(f'./NewData/CleanedForm/{meeting} - Form.csv', index=0)

pfratings_path = r'./NewData/Ratings/'
pf_ratings = pd.read_csv(pfratings_path + f"{etd} - RatingsSheet.csv", index_col=False, header=0)

pf_field = pd.read_csv(f'./NewData/Fields/{etd} - Fields.csv', index_col=0)
pf_field.rename(columns={' Horse':'Horse', ' Tab Number':'Tab Number', ' Weight':'Weight', ' Claim':'Claim', ' Jockey':'Jockey', ' Trainer':'Trainer'}, inplace=True)

race = pd.merge(pf_field, pf_ratings, how='left',left_on=['Horse','Tab Number'],right_on=['HorseName','TabNo'])

race = race.reset_index(drop=True)
race.drop([' HorseId', ' TrainerId', ' FormId', ' Barrier', 'RaceNo', 'HorseName', 'TabNo'], axis=1, inplace=True)

pf_form = pd.read_csv(f'./NewData/CleanedForm/{etd}-{track} - Form.csv', index_col=0)

races = pd.merge(race, pf_form, how='left', left_on=['Horse', 'Tab Number', 'Meeting'], right_on=['horse name', 'horse number', 'track'])

races1 = pd.merge(races, form_df3, how='left', left_on=['Horse', 'Tab Number', 'Race Number'], right_on=['Horse', 'Tab Number', 'Race Number'])

races2 = pd.merge(races1, form_df6, how='left', left_on=['Horse', 'Tab Number', 'Race Number'], right_on=['Horse', 'Tab Number', 'Race Number'])

races2 = races2.dropna(axis=0, subset=['Barrier'])

races2.rename(columns={'form position':'Form Pos-1', 'form margin':'Form Margin-1', 'HorseName':'Horse', 'Tab Number':'Tab No', 'form price':'Form Price-1', 'TrackCondition':'Tr-Cond', 'Historical Run Style':'Hist Run Style', 'distance':'Distance', 'form track':'Form Track-1', 'form tack condition':'Form Tr Cond-1', 'form barrier':'Form Barrier-1', 'form distance':'Form Dist-1', 'Predicted Settling Position':'Pred Stlg Pos', 'horselast10':'Form Last 10', 'form weight':'Form Weight-1', 'form class':'Form Cl-1', 'form jockey':'Form Jky-1', 'form meeting date':'Form Mtg Date', 'form other runners':'Form Other Runners-1', 'form time':'Form Time-1', 'form track condition':'Form Tr-Cond-1', 'class restrictions':'Race Cl', 'horse record':'Horse Record', 'horse record track':'Record Track', 'horse record distance':'Record Dist', 'horse record track distance':'Record Trk-Dist', 'horse record firm':'Record Firm', 'horse record good':'Record Good', 'horse record soft':'Record Soft', 'horse record heavy':'Record Heavy', 'horse record first up':'First Up Record', 'horse record second up':'Second Up Record', ' RaceId':'RaceId'}, inplace=True)

races2.drop(['race number', 'horse name', 'horse number', 'horse barrier', 'horse jockey', 'horse trainer', 'horse weight', 'horse claim', 'form name', 'horse record jumps'], axis=1, inplace=True)

races2['Pred Stlg Pos'].replace('-',99, inplace=True)
races2['Neural Price'].replace('-',99, inplace=True)
races2['Class Change'].replace('-',99, inplace=True)

columns = ['Pred Stlg Pos', 'Dist SR', 'Neural Price', 'Class Change']
races2[columns] = races2[columns].astype(float)

races2['Wght Chg'] = races2['Weight'] - races2['Form Weight-1']
races2['Dist Chg'] = races2['Distance'] - races2['Form Dist-1']
races2['Bar Chg'] = races2['Barrier'] - races2['Form Barrier-1']

races2['Form Mtg Date'] =  pd.to_datetime(races2['Form Mtg Date'])
races2['Form Mtg Date'] = races2['Form Mtg Date'].dt.strftime('%d-%m-%Y')

cols = ['Time', 'Race Cl', 'Distance', 'Meeting', 'Tr-Cond']
races2[cols] = races2[cols].ffill(axis=0)

races2['DBR-1/2'] = races2['DLR-2'] - races2['DLR-1']
races2['DBR-2/3'] = races2['DLR-3'] - races2['DLR-2']

races2['Horse'] = races2['Horse'].str.replace(r"[\"\',]", '')
races2['Horse'] = races2['Horse'].str.title()

races2['Starters'] = (races2.groupby(["Meeting", "Race Number"])['Tab No'].transform('nunique'))

races3 = races2[['Meeting', 'Race Number', 'Distance', 'Tab No', 'Horse', 'HorseId', 'Weight', 'Barrier', 'Jockey', ' JockeyId', 'Trainer', 'Tr-Cond', 'Class Change', 'Hist Run Style', 'Pred Stlg Pos', 'Neural Rank', 'age restrictions', 'Race Cl', 'weight restrictions', 'sex restrictions', 'weight type', 'horse age', 'Race Starts', 'horse sex', 'Form Margin-1', 'Form Pos-1', 'Form Price-1', 'Starters']]

races3.rename(columns={'Tr-Cond': 'Trackcondition', 'Pred Stlg Pos':'Settling Pos', 'Neural Rank':'Neural', 'weight restrictions':'Limitweight', 'weight type':'Weighttype', 'horse age':'Age', 'horse sex':'Sex', 'Form Margin-1':'Margin', 'Form Pos-1':'LSFinPos', 'Form Price-1':'LSSP', 'HorseId':'Horseid', ' JockeyId':'Jockeyid', 'Race Starts':'Rno'}, inplace=True)

races2.to_csv('./NewData/%s.csv' %meeting, index=False)
races2.to_excel('./NewData/%s.xlsx' %meeting, index=False)

races3.to_csv(f'./NewData/Test/{etd}-TestFile.csv', index=False)




# Predicting code


# Load the saved model
model = tf.keras.models.load_model('my_model.h5')

# Load the pickled XGB model
with open('XGB.pkl', 'rb') as f:
    classifier = pk.load(f)

# Load the pickled XGB feature columns
with open('xgb_cols.pkl', 'rb') as f:
    xgb_cols = pk.load(f)

with open('LSTM_cols.pkl', 'rb') as f:
    LSTM_cols = pk.load(f)

with open('encoders.pkl', 'rb') as f:
    encs = pk.load(f)

def predict(X):
    xgb_preds = classifier.predict(X[xgb_cols])
    lstm_preds = model.predict(X).reshape(xgb_preds.shape)

    return (xgb_preds + lstm_preds) / 2


btdays = 0
today = date.today()
rundate = today - timedelta(days=btdays)
dte = rundate.strftime('%d-%m-%Y')
etd = rundate.strftime('%Y-%m-%d')

tst_df_full = pd.read_csv(f'./NewData/Test/{etd}-TestFile.csv').dropna()

tst_df = tst_df_full.rename(columns={
    'Meeting': 'Meetingid',
    'Race Number': 'Raceid',
    'Race Cl': 'Class',
    'age restrictions': 'Agerestrictions',
    'sex restrictions': 'Sexrestrictions',
    'Tab No': 'Tabno'
})[LSTM_cols]

cat_cols = [col for col in tst_df.columns if tst_df[col].dtype == 'object']
for col in cat_cols:
    tst_df[col] = encs[col].transform(tst_df[col].astype(str))

tst_df_full['preds%'] = predict(tst_df) * 100
tst_df_full['preds%'][tst_df_full['preds%'] > 100] = 100
tst_df_full['preds%'][tst_df_full['preds%'] < 0] = 0

tst_df_full.to_csv(f'Predictions/{etd}-Predictions.csv', index=False)