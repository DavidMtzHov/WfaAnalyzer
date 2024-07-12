import streamlit as st
from functions import * 
import time

st.title("CSV Analyzer")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if 'counter' not in st.session_state:
    st.session_state.counter = 0

if 'csv_format' not in st.session_state:
    st.session_state.csv_format = 'European (separator=";" and decimal=",")'

if 'date_hint' not in st.session_state:
    st.session_state.date_hint = 'YYYY-MM-DD HH:MM:SS'

if st.session_state.counter >= 0 and st.session_state.counter <= len(questions):   
    #project configuration upload
    if st.button('Clear Configurations',use_container_width=True):
        st.error('Do you want to delete the project upload configurations?')
        c1,c2,c3,c4 = st.columns(4)
        with c2:
            no = st.button('No')
        with c3:
            yes = st.button('Yes',on_click=delete_config)

    col1,col2 = st.columns(2)
    with col1:
        st.session_state.csv_format = st.selectbox(
            "Select the CSV file format",
            ('Traditional (separator="," and decimal=".")', 
                'European (separator=";" and decimal=",")'),
            index=1
        )
    with col2:
        st.session_state.date_hint = st.selectbox("Optional: Date Time Format",dts)

if uploaded_file is not None:
    data = StringIO(uploaded_file.getvalue().decode("utf-8"))
    
    df = load_data(data, st.session_state.csv_format)
    
    date_column, date_format = detect_datetime_format(df, st.session_state.date_hint)

    #Data Preview
    if st.session_state.counter >= 0 and st.session_state.counter <= len(questions)+1:        
        st.write("Upload Data Preview:")
        st.write(df.head())

    #Configuration
    if st.session_state.counter >= 0 and st.session_state.counter < len(questions):
        st.write(questions[st.session_state.counter])
        c1,c2,c3,c4,c5 = st.columns(5)
        with c2:
            if st.button('Yes'):
                st.session_state.counter += 1
                time.sleep(0.05)
                st.rerun()
        with c3:
            if st.button('No'):
                st.session_state.counter += 1
                time.sleep(0.05)
                st.rerun()
        with c4:
            if st.button('Prev'):
                st.session_state.counter -= 1
                if st.session_state.counter<0:
                    st.session_state.counter = 0
                time.sleep(0.05)
                st.rerun()
    elif st.session_state.counter == len(questions):
        c1,c2,c3 = st.columns(3)
        with c2:
            st.write('Thank you!')
            if st.button('Save and submit',use_container_width=True,type='primary'):
                st.session_state.counter += 1
                time.sleep(0.05)
                st.rerun()
        c1,c2,c3 = st.columns(3)
        with c2:
            if st.button('Prev',use_container_width=True):
                st.session_state.counter -= 1
                if st.session_state.counter<0:
                    st.session_state.counter = 0
                time.sleep(0.05)
                st.rerun()
    else:
        numerical_df = df.select_dtypes(include=['number'])   
        non_value_cols = st.sidebar.multiselect('Choose non value columns, in case wrongly identified.',numerical_df.columns)

        if non_value_cols:
            cols = numerical_df.columns.to_list()
            for item in non_value_cols:
                cols = [c for c in cols if item not in c]
            numerical_df = numerical_df[cols]
            for item in non_value_cols:
                df[item] = df[item].astype(str)

        
        hierarchy_columns = st.sidebar.multiselect('Choose Hierarchy columns:',df.select_dtypes(include=['object']).columns)
        value_column = st.sidebar.selectbox('Choose value column:',df.select_dtypes(include=['float','int']).columns)
        datetime_column= st.sidebar.selectbox('Choose date time column from:',df.select_dtypes(include=['datetime']).columns)