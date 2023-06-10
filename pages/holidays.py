import holidayapi
import streamlit as st

#no waiting to compile

key = 'b3550910-91ef-4071-8272-390dcd4f51e2'
hapi = holidayapi.v1(key)



if st.button("start"):
    holidays = hapi.holidays({
        'country': 'LK',
        'year': '2022',
})

if holidays['status'] == 200:
    for holiday in holidays['holidays']:
        name = holiday['name']
        date = holiday['date']
        public = holiday['public']
        observed = holiday['observed']
        weekday_date = holiday['weekday']['date']['name']
        weekday_observed = holiday['weekday']['observed']['name']
        data = holidays["holidays"]
        st.write(data)
        # st.write(f"Name: {name}")
        # st.write(f"Date: {date}")
        # st.write(f"Public: {public}")
        # st.write(f"Observed: {observed}")
        # st.write(f"Weekday (Date): {weekday_date}")
        # st.write(f"Weekday (Observed): {weekday_observed}")
        # # print()
else:
    print("Failed to retrieve holiday information.")
