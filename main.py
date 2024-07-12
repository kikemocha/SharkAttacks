import pandas as pd
import numpy as np
import re
import ollama
from tqdm import tqdm

tqdm.pandas()
"""
Rows => 6944
Columns => 14

['Date', 'Year', 'Type', 'Country', 'State', 'Location', 'Activity',
'Name', 'Sex', 'Age', 'Injury', 'Time', 'Species ', 'Source']

"""

"""
Taks:

Types -> Solo strip el Provoked

"""
def clean_times(time):
    dictionary = {
        'afternoon':'14:00', 
        'morning':'8:00',
        'dusk': '20:00',
        'night': '23:00',
        'late afternoon': '18:00',
        'p.m.' : '12:00',
        'a.m' : '4:00',
        'midday' : '12:00',
        'early morning': '6:00',
        'early afternoon' : '13:00',
        'sunset' : '19:00'
        }
    return time

def categorize_with_model(user_message):
    try:
        response = ollama.chat(model='mistral', messages=[
            {
                'role': 'user',
                'content' : f'This sentence is a description of a shark attack I want you to classify this sentence({user_message}) in "Mortal" or "No Mortal", return only one value. If is "Fatal" it is Mortal If information is not enough to determinate if its mortal or not mortal return "Nan", but it is important to only return one word'
            },
        ])
        if 'message' in response and 'content' in response['message']:
            # Imprimir la respuesta del modelo
            return response['message']['content']
        else:
            return "Error: Respuesta inesperada del modelo."
        
    except Exception as e:
        return f"Error: {e}"

url = 'GSAF.csv'
df = pd.read_csv(url)
"""
print(df.shape)
df = df.drop(['Unnamed: 11','pdf','href formula','href','Case Number','Case Number.1', 'original order', 'Unnamed: 21', 'Unnamed: 22'], axis=1)
df = df.drop(range(6944,6969),axis=0)
print(df.columns)
print(df['Time'].value_counts()[80:120])
print()
print(df.tail())
"""
dict_ages = {
    'teen': 14, 
    'young': 7,
    'teens': 14,
    'elderly': 80,
    'adult': 50
    }


test = df[df['Age'].apply(lambda x : str(x).isdigit())]
test['Age'] = test['Age'].apply(lambda x : int(x))
mean = test['Age'].mean()

def clean_ages(ages):
    if str(ages).isdigit():
        return int(ages)
    elif ages in dict_ages:
        return dict_ages[ages]
    else:
        return mean

df['Age'].fillna(mean, inplace=True)
df['Age'] = df['Age'].apply(lambda x : clean_ages(x))

regex_pattern = r'(\d{2})\s*([A-Za-z]{3})\s*(\d{4})|(\d{2})-([A-Za-z]{3})-(\d{4})|(\d{2})\s([A-Za-z]{3})-(\d{4})|(\d{2})-([A-Za-z]{3})\s(\d{4})|(\d{2})\s([A-Za-z]{3})--(\d{4})'
regex_pattern2 = r'(^[A-Za-z]{3})-(\d{4})|(^[A-Za-z]{3})\s(\d{4})'
fechas = [
    '15 Mar 2024',
    '14-Jul-2021',
    '25 Feb-2024',
    '29 Jan--2023',
    'Reported 28-Aug-2018'
]
def extract_date_components(date_str):
    try:
        if pd.isna(date_str):
            return np.nan
        else:
            match = re.search(regex_pattern, date_str)
            if match:
                # Verifica cuál de los patrones ha coincidido y extrae los componentes

                if match.group(1):
                    day, month, year = match.group(1), match.group(2), match.group(3)
                elif match.group(4):
                    day, month, year = match.group(4), match.group(5), match.group(6)
                elif match.group(7):
                    day, month, year = match.group(7), match.group(8), match.group(9)
                elif match.group(10):
                    day, month, year = match.group(10), match.group(11), match.group(12)
                else:
                    return np.nan
                return f"{day}/{month}/{year}"
            else:
                match2 = re.search(regex_pattern2, date_str)
                if match2:
                    if match2.group(1):
                        month, year = match2.group(1), match2.group(2)
                    elif match2.group(3):
                        month, year = match2.group(3), match2.group(4)
                    else:
                        return np.nan
                    return f"1/{month}/{year}"
            return np.nan
    except Exception as error:
        print(date_str, error)
        return np.nan


df['Date'] = df['Date'].apply(lambda x : extract_date_components(str(x)))
df.dropna(subset=['Date'], inplace=True)

df['Date'] = pd.to_datetime(df['Date'], format="%d/%b/%Y", errors='coerce')
df['Month'] = df['Date'].dt.strftime('%b')
df_aux = df.pivot_table(index=['Country','Month'], values='Date', aggfunc=['count']).reset_index()
df_country_month = df_aux[(df_aux['Country'].isin(['USA','SOUTH AFRICA','AUSTRALIA']))]

mode = df['Age'].mode()
def categorize(age):
    try:
        if age <= 12:
            return "Child"
        elif age > 12 and age <= 18:
            return "Teen"
        elif age > 18 and age <= 60:
            return "Adult"
        elif age > 60:
            return "Senior"
        else:
            return "Adult"
    except:
        return "Adult"
df['Age_Grouped'] = df['Age'].apply(categorize)
df['Age_Grouped'].isna().sum()

df['Injury'] = df['Injury'].progress_apply(lambda x :  categorize_with_model(x))
df.to_csv('clean_dataset.csv', index=False)