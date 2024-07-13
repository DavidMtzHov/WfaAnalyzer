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
    if st.checkbox('Format Upload data'):
        configurations = pd.read_json('config.json')
        if 'answers' not in st.session_state:
             st.session_state.answers = configurations
        if len(configurations[configurations['answers'].isna() == True])>0:
            if st.session_state.counter >= 0 and st.session_state.counter < len(questions):
                st.write(questions[st.session_state.counter])
                c1,c2,c3,c4,c5 = st.columns(5)
                if c2.button('Yes'):
                        st.session_state.answers.iloc[st.session_state.counter,1] = 1
                        st.session_state.counter += 1
                        time.sleep(0.05)
                        st.rerun()
                if c3.button('No'):
                        st.session_state.answers.iloc[st.session_state.counter,1] = 0
                        st.session_state.counter += 1
                        time.sleep(0.05)
                        st.rerun()
                if c4.button('Prev'):
                        st.session_state.counter -= 1
                        if st.session_state.counter<0:
                            st.session_state.counter = 0
                        time.sleep(0.05)
                        st.rerun()
            elif st.session_state.counter == len(questions):
                st.write(st.session_state.answers)
                c1,c2,c3 = st.columns(3)
                c2.write('Thank you!')
                if c2.button('Save and submit',use_container_width=True,type='primary'):
                    st.session_state.answers.to_json('config.json')
                    st.session_state.counter += 1
                    time.sleep(0.05)
                    st.rerun()
                c1,c2,c3 = st.columns(3)
                if c2.button('Prev',use_container_width=True):
                        st.session_state.counter -= 1
                        if st.session_state.counter<0:
                            st.session_state.counter = 0
                        time.sleep(0.05)
                        st.rerun()
        elif st.session_state.counter > len(questions):
            if configurations.iloc[0,1] == 1:
                numerical_df = df.select_dtypes(include=['number'])   
                non_value_cols = st.multiselect('Choose coulmns that should be text.',numerical_df.columns)

                if non_value_cols:
                    cols = numerical_df.columns.to_list()
                    for item in non_value_cols:
                        cols = [c for c in cols if item not in c]
                    numerical_df = numerical_df[cols]
                    for item in non_value_cols:
                        df[item] = df[item].astype(str)
            if configurations.iloc[1,1] == 1:
                values = st.selectbox('Choose Value Column.',df.select_dtypes(include=['number']).columns)
                column = st.selectbox('Choose pivot column.',df.select_dtypes(include=['object']).columns)
                ix = df.select_dtypes(include=['object']).columns.to_list()
                ix = [item for item in ix if column != item]
                if values and column:
                    try:
                        df = df.pivot_table(index=ix,values=values,columns=column).reset_index()
                    except:
                        st.write('Problem with input variables, unable to Pivot table.')
            if configurations.iloc[2,1] == 1:
                idvar = st.multiselect('Select id variables.',df.select_dtypes(include=['object']).columns)
                valuevar = st.multiselect('Select value variables.',df.select_dtypes(include=['number']).columns)
                varname = st.text_input('Please enter variable name.')
                valname = st.text_input('Please enter value name.')
                if idvar and valuevar and varname and valname:
                    try:
                        df = pd.melt(df,id_vars=idvar,value_vars=valuevar,var_name=varname,value_name=valname).reset_index()
                    except:
                        st.write('Problem with input variables, unable to Melt table.')

            
            hierarchy_columns = st.multiselect('Choose Hierarchy columns:',df.select_dtypes(include=['object']).columns)
            value_column = st.selectbox('Choose value column:',df.select_dtypes(include=['float','int']).columns)
            datetime_column= st.selectbox('Choose date time column from:',df.select_dtypes(include=['datetime']).columns)
        else:
            #project configuration upload
            st.write('Project has configured format.')
            if st.button('Clear Configurations',use_container_width=True):
                st.error('Do you want to delete the project upload configurations?')
                c1,c2,c3,c4 = st.columns(4)
                c2.button('No!')
                c3.button('Yes!',on_click=delete_config)