import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
from llama_index import download_loader
from pandasai.llm.openai import OpenAI
import datetime

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# List of initial keywords
initial_keywords = ['Galle Tourism', 'Galle', 'Hotels Galle', 'Resorts Galle Srilanka', 'Srilanka', 'Tourist', 'locations']

# Create a for keyword selection
selected_keywords = st.multiselect('Select existing keywords', initial_keywords)

# Allow additional keywords to be added
additional_keyword = st.text_input("Add a new keyword")
if additional_keyword:
    selected_keywords.append(additional_keyword)

# Initialize the AI
llm = OpenAI()
PandasAIReader = download_loader("PandasAIReader")
loader = PandasAIReader(llm=llm)

# When keywords are selected, fetch data from Google Trends and display it
if st.button('Fetch Google Trends data for selected keywords'):
    # Get the current year
    current_year = datetime.datetime.now().year

    # Calculate the previous year
    previous_year = current_year - 1

    # Define the timeframe
    timeframe = f'{previous_year}-01-01 {previous_year}-12-31'

    # Get Google Trends data
    pytrends.build_payload(selected_keywords, timeframe=timeframe)

    # Get interest over time
    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(labels=['isPartial'], axis='columns')

        # Save the data to the session state
        st.session_state.data = data

        st.write(data)
else:
    # If the data is already in the session state, load it
    if 'data' in st.session_state:
        data = st.session_state.data
        st.write(data)

# Assuming you want to use the AI to answer questions based on the fetched data
query = st.text_input("Enter your question")
ask = st.button("Ask")

if ask:
    # Check if data is available
    if 'data' in st.session_state:
        data = st.session_state.data

        # Check if data is not empty
        if not data.empty:
            # Fetch the most recent data based on the date range
            timeframe_start = data.index.min().strftime('%Y-%m-%d')
            timeframe_end = data.index.max().strftime('%Y-%m-%d')
            timeframe = f'{timeframe_start} {timeframe_end}'
            pytrends.build_payload(selected_keywords, timeframe=timeframe)
            updated_data = pytrends.interest_over_time()
            if not updated_data.empty:
                updated_data = updated_data.drop(labels=['isPartial'], axis='columns')
                data = pd.concat([data, updated_data])

        response = loader.run_pandas_ai(data, query, is_conversational_answer=True)
        st.write(response)
    else:
        st.write("Please fetch Google Trends data first.")
