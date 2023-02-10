from book import NTUBadmintonCourt
import streamlit as st
import datetime

def date_time_court_to_button_value(date, time, court):
    return f"1BB2BB{court}{date}{time}"

time_to_index_dict = {'10-11' : '3','11-12' : '4','12-13' : '5','13-14' : '6','14-15' : '7','16-17' : '9','17-18' : '10','18-19' : '11','19-20' : '12','20-21' : '13','21-22' : '14'}

# streamlit date
date = st.date_input("Date", value=datetime.date.today() + datetime.timedelta(days=8), min_value=datetime.date.today(), max_value=datetime.date.today() + datetime.timedelta(days=7))
date_str = date.strftime("%d-%b-%Y")

# select time
time = st.selectbox("Time", options=['10-11','11-12','12-13','13-14','14-15','16-17','17-18','18-19','19-20','20-21','21-22'])
time_str = time_to_index_dict[time]

# select court
court = st.selectbox("Court", options=['01','02','03','04','05','06'])

account = st.text_input("Account", value="")
password = st.text_input("Password", value="")

headless = st.sidebar.checkbox("Headless(don't show chrome)", value=False)
chrome_version = st.sidebar.text_input("Chrome Version(make sure same as your chrome)", value="109")
max_retry = st.sidebar.text_input("Max Retry", value="1000")

# start
if st.button("Confirm"):
    button_value = date_time_court_to_button_value(date_str, time_str, court)
    st.write(f'button value: {button_value}   Excuting......')
    badminton = NTUBadmintonCourt(account=account, password=password, headless=headless, chrome_version=chrome_version)
    badminton.open_badminton_page()
    if badminton.run(button_value=button_value, max_retry=int(max_retry)):
        st.title("Success")
    else:
        st.title("Fail")






