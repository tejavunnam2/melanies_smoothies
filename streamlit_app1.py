import streamlit as st
from snowflake.snowpark.functions import col

import requests
# Write directly to the app
st.title("customize your smoothie")
st.write(
    """choose the fruits in your custom smoothie
    """
)

cnx =st.connection("snowflake")

session=cnx.session()
my_dataframe=session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('fruit_name'))
name_on_order=st.text_input("name on smoothie")
st.write("name on smoothie is",name_on_order)
options = st.multiselect(
    "choose 5 fruits",
    my_dataframe,max_selections=5)
if options:
    st.write("You selected:", options)
    list=''
    for x in options:
        list+=x+' '
    st.write(list)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + list + """','""" + name_on_order + """')"""

    time_to_insert=st.button('submit')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+name_on_order+'!', icon="✅")
	    
