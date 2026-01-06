import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import gdown

st.title('Mini AutoML (Cross-Sectional) v1.0')

df_pp = None

uploaded_file = st.file_uploader("Upload a '.csv' or '.xlsx' file", type = ['csv', 'xlsx'], accept_multiple_files = False)
if uploaded_file:
  try:
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

  st.write('### Data Preview')
  st.dataframe(df_pp.head())
else:
  st.write('### No file upload detected')
  
