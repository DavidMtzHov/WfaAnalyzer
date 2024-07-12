import streamlit as st
import pandas as pd
from io import StringIO

@st.cache_data
def load_data(data, csv_format):
    if csv_format == 'Traditional (separator="," and decimal=".")':
        return pd.read_csv(data, sep=",", decimal=".")
    else:
        return pd.read_csv(data, sep=";", decimal=",")
    
#User displayed formats
dts = ['YYYY-MM-DD HH:MM:SS','YYYY-MM-DD HH:MM','YYYY-MM-DD','YY-MM-DD HH:MM:SS','YY-MM-DD HH:MM','YY-MM-DD','DD.MM.YYYY HH:MM:SS','DD.MM.YYYY HH:MM','DD.MM.YYYY','DD.MM.YY HH:MM:SS','DD.MM.YY HH:MM','DD.MM.YY HH:MM:SS']
#Python time formats
pydts = ["%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M", "%Y-%m-%d","%y-%m-%d %H:%M:%S","%y-%m-%d %H:%M","%y-%m-%d", "%d.%m.%Y %H:%M:%S","%d.%m.%Y %H:%M","%d.%m.%Y","%d.%m.%y %H:%M:%S","%d.%m.%y %H:%M","%d.%m.%y"]
    

def detect_datetime_format(df, date_hint):
    sd = dict(zip(dts,pydts))
    sd = sd[date_hint]
    
    for column in df.columns:
        try:
            df[column] = pd.to_datetime(df[column], format=sd)
        except (ValueError, TypeError):
            continue
    return column,sd

@st.cache_data
def df_information(df):
    return df.describe()

def delete_config():
    st.success('Project Upload configurations deleted.')

questions = ['Were text columns identified as numbers?','Do you need to pivot rows?','Do you need to pivot columns?',
             'Do you need to add time to a date field?',]