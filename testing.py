import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import gdown
import textwrap as tw

# Title call
st.title('Mini AutoML (Cross-Sectional) v1.0')

# Dataset upload and conversion to a pandas dataframe
df_pp = None

uploaded_file = st.file_uploader("Upload a '.csv' or '.xlsx' file", type = ['csv', 'xlsx'], accept_multiple_files = False)
if uploaded_file:
  try:
    file_name = uploaded_file.name
    if uploaded_file.name.endswith('.csv'):
      df_pp = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
      df_pp = pd.read_excel(uploaded_file)
  except:
    st.error("Uploaded file format must be in either '.csv' or '.xlsx'")
else:
  st.info('Upload a file of the requested format from local to begin the analysis', icon = 'ℹ️')

st.write('OR')

file_id = st.text_input('Input shared Google Drive file ID (e.g. 1Fq32N3GU...)')
file_name = st.text_input("Input shared Google Drive file name (including '.csv'/'.xlsx' extension)")
if file_id != '' and file_name != '':
  if st.button('Download shared file'):
    file_url = f'https://drive.google.com/uc?id={file_id}'
    uploaded_file = gdown.download(file_url, file_name, quiet = True)
    try:
      if file_name.endswith('.csv'):
        df_pp = pd.read_csv(uploaded_file)
      elif file_name.endswith('.xlsx'):
        df_pp = pd.read_excel(uploaded_file)
    except:
      st.error("Uploaded file format must be in either '.csv' or '.xlsx'")
else:
  st.info('Link a shared Google Drive file of the requested format to begin the analysis', icon = 'ℹ️')

if df_pp is not None:

  # Dataset unusable column and white space cleaning
  initial_columns = [col for col in df_pp.columns]
  for col in initial_columns:
    if col.startswith('Unnamed:') or len(df_pp) == df_pp[col].isna().sum() or df_pp[col].nunique() == 1:
      df_pp.drop(col, axis = 1, inplace = True)

  initial_columns = [col for col in df_pp.columns]
  for col in initial_columns:
    if df_pp[col].dtypes == object:
      df_pp[col] = df_pp[col].str.strip()
    if col != col.strip():
      df_pp = df_pp.rename(columns = {col: col.strip()})
  
  # Dataset's variable type specification setup
  st.write('### ---- SETUP ----')
  st.write('✅ — Dataset upload and conversion to pandas dataframe complete!')
  st.write('✅ — Dataset unusable column cleaning complete!')
  st.write(f'{file_name} Data Preview:')
  st.dataframe(df_pp.head())
  st.write(f'⋯ {len(df_pp)} initial rows for analysis!')
  st.write(tw.dedent(
      '''
      Specify column data type!

      * Specify 'Nominal' for classification target variable
      * Apply 'ID' labeling only to a single column
      * Incorrect data type input would result in an error
      '''
  ).strip())
  col_names = [col for col in df_pp.columns]
  col_types = []
  id_count = 0
  for col in col_names:
    data_type = st.selectbox(f"'{col}' column data type (input) is:", ['Identification (ID)', 'Continuous/Float', 'Discrete/Integer', 
                                                                       'Ordinal', 'Nominal', 'Column Drop/Unused'], accept_new_options = False)
    if data_type == 'Identification (ID)':
      id_count = id_count + 1
      if id_count >= 2:
        st.error('ID label has been assigned to 2 or more columns')
    col_types.append(data_type.lower())
  st.write('✅ — Dataset variable type specification complete!')

  # Random sampling in the case of large population

  st.write('### Data Preview')
  st.dataframe(df_pp.head())

else:
  st.write('### No file upload detected')
  
