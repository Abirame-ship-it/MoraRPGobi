import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
from llama_index import download_loader
from pandasai.llm.openai import OpenAI

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# List of initial keywords
initial_keywords = ['Galle Tourism', 'Galle', 'Hotels Galle', 'Resorts Galle Srilanka','Srilanka', 'Tourist', 'locations']

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
    # Define the payload
    kw_list = selected_keywords

    # Get Google Trends data
    pytrends.build_payload(kw_list, timeframe='all')

    # Get interest over time
    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(labels=['isPartial'],axis='columns')

        st.write(data)

        # Assuming you want to use the AI to answer questions based on the fetched data
        query = st.text_input("Enter your question")
        if query:
            response = loader.run_pandas_ai(data, query, is_conversational_answer=False)
            st.write(response)

    else:
        st.write('The selected keywords do not have enough data to display a trend.')
