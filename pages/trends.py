import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
from llama_index import download_loader
from pandasai.llm.openai import OpenAI
import datetime




# if holidays['status'] == 200:
#     for holiday in holidays['holidays']:
#         name = holiday['name']
#         date = holiday['date']
#         public = holiday['public']
#         observed = holiday['observed']






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

    key = 'b3550910-91ef-4071-8272-390dcd4f51e2'
    hapi = holidayapi.v1(key)
    holidays = hapi.holidays({
        'country': 'LK',
        'year': '2022',
    })


    pytrends.build_payload(kw_list, timeframe='today 5-y')

        # Get interest over time
    data = pytrends.interest_over_time()

    if not data.empty:
        names = [entry['name'] for entry in holidays["holidays"]]
        dates = [entry['date'] for entry in holidays["holidays"]]

        # Create a new DataFrame with extracted data
        new_df = pd.DataFrame({'date': dates, 'name': names})

        # Merge the new DataFrame with the existing DataFrame based on the date column
        data = data.merge(new_df, on='date', how='left')

        data = data.drop(labels=['isPartial'],axis='columns')

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
        st.session_state.data = data

        # Check if data is not empty
      
        response = loader.run_pandas_ai(data, query, is_conversational_answer=True)
        st.write(response)
    else:
        st.write("Please fetch Google Trends data first.")
