import streamlit as st
import requests
import pandas as pd


st.set_page_config(page_title="FRED Extract", page_icon=":seedling:", menu_items=None)
# Your FRED API key
api_key = "e0dd9407e778e6ce81f78adf2bb1fcf1"

# URL to fetch US GDP data from FRED API
url = f"https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key={api_key}&file_type=json"

# Fetch the GDP data
response = requests.get(url)
gdp_data = response.json()

## Display the GDP data in Streamlit
st.title("US GDP Data from FRED API")
# st.json(gdp_data)

# Display the data in a table format if observations are available
if "observations" in gdp_data:
    observations = gdp_data["observations"]
    data = [{"Date": obs["date"], "GDP Value": obs["value"]} for obs in observations]
    df = pd.DataFrame(data)
    # Reset the index to remove the default index column
    df = df.reset_index(drop=True)

    # Convert DataFrame to a list of dictionaries
    records = df.to_dict('records')

    st.write("GDP Data:")
    # Use st.table to display the table without the index
    st.table(records)