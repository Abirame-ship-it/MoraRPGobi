import streamlit as st
from pathlib import Path
from llama_index import download_loader
import pandas as pd
from pandasai.llm.openai import OpenAI
import os

# Initialize the AI
llm = OpenAI()
PandasAIReader = download_loader("PandasAIReader")
loader = PandasAIReader(llm=llm)
st.subheader("Sentimental Analysis-chat")

# Define the path to your CSV file
# file_path = Path('Preprocessingdata.csv')
patj = os.path.join('data','PreprocessedData (1).csv')
# st.write(patj)
# Read the CSV file into a pandas DataFrame
df = pd.read_csv(patj)

# Display the DataFrame
st.write(df)

# Get a question from the user
query = st.text_input("Enter your question")

if query:
    response = loader.run_pandas_ai(df, query, is_conversational_answer=True)
    st.write(response)
