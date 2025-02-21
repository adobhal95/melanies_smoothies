# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("🥤Customize Your Smoothie!🥤")
name_on_order = st.text_input("Name on Smoothie:")
st.write("Name on the Smoothie will be:",name_on_order)
st.write(
    """
    Choose the fruits you want in your custom Smoothie
    """
)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe,use_container_width=True)
# st.stop()

# snowpark datafrome -> pandas dataframe 
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredient_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)
if ingredient_list and name_on_order:
    st.text(ingredient_list)
    ingredient_string = ''
    for fruit_choosen in ingredient_list:
        ingredient_string += fruit_choosen+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        sf.subheader(fruit_choosen+' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_choosen)
        sf_df = st.dataframe(smoothiefroot_response.json(),use_container_width=True)
    #st.write(ingredient_string)
    my_insert_stmt = """
    insert into smoothies.public.orders(ingredients,name_on_order) 
    values('""" + ingredient_string + """','""" + name_on_order + """');
    """
    #st.write(my_insert_stmt)
    time_to_order = st.button('Submit Order')
    if time_to_order:
        if not ingredient_string:
            st.error('ingredient list is empty', icon="🚨")
        session.sql(my_insert_stmt).collect()
        st.success(f'Your smoothies is ordered, {name_on_order}!',icon='✅')

# st.text(smoothiefroot_response.json())

