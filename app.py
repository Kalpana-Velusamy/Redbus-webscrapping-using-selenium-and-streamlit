# importing libraries
import pandas as pd
import mysql.connector
import streamlit as slt
from streamlit_option_menu import option_menu
import plotly.express as px

def fetch_details(query):
    conn = mysql.connector.connect(host="localhost", user="root", password="Amyshik@0906", database="red_bus_details")
    my_cursor = conn.cursor()
    my_cursor.execute(query)
    data = my_cursor.fetchall()
    conn.close()

    return data

def fetch_busses(time_range, state, route, bus_type, price_range):
    if price_range == "50-1000":
        price_min, price_max = 50, 1000
    elif price_range == "1000-2000":
        price_min, price_max = 1000, 2000
    elif price_range == "Any":
        price_min, price_max = 50, 100000
    else:
        price_min, price_max = 2000, 100000

    if bus_type == "sleeper":
        bus_type_condition = "bus_type LIKE '%Sleeper%'"
    elif bus_type == "semi-sleeper":
        bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
    elif bus_type == "Any":
        bus_type_condition = "bus_type IS NOT NULL"
    else:
        bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

    query = f'''
            SELECT 
             bus_name, bus_type, departure_at, arrival_at, duration,
            price, seats, rating
               FROM bus_details
            WHERE price BETWEEN {price_min} AND {price_max}
            AND route_name = "{route}"
            AND state_name = "{state}"
            AND {bus_type_condition} AND departure_at>='{time_range}'
            ORDER BY price and departure_at DESC
        '''
    data = fetch_details(query);
    df = pd.DataFrame(data, columns=[
             "Travels Name", "Bus Type", "Departure Time", "Arrival Time", "Duration",
            "Price", "Seats Available", "Rating"
        ])
    return df

def fetch_state():
    query = f'''
            SELECT state_name FROM bus_details
            GROUP BY state_name
        '''
    data = fetch_details(query);
    states = [row[0] for row in data] 
    return states

def fetch_routes(state):
    query = f'''
            SELECT route_name FROM bus_details
            where state_name ="{state}"
            GROUP BY route_name
        '''
    data = fetch_details(query);
    routes = [row[0] for row in data] 
    return routes

details_df=pd.read_csv("formatted_df.csv")

slt.set_page_config(layout="wide")

web=option_menu(menu_title="RedBus Online Booking",
                options=["Home","Bus Search"],
                icons=["house","bus-front"],
                orientation="horizontal"
                )
# Home page setting
if web=="Home":
    
    slt.title("Redbus Data Scraping using Selenium And Dynamic Filtering using Streamlit")
    slt.subheader(":red[Domain:]  Transportation")
    slt.subheader(":red[Ojective:] ")
    slt.markdown("The 'Redbus Data Scraping and Filtering with Streamlit Application' aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry.")
    slt.subheader(":red[Overview:]")
    slt.markdown("Selenium: Selenium is a tool used for automating web browsers. It is commonly used for web scraping, which involves extracting data from websites. Selenium allows you to simulate human interactions with a web page, such as clicking buttons, filling out forms, and navigating through pages, to collect the desired data.")
    slt.markdown('''Pandas: Use the powerful Pandas library to transform the dataset from CSV format into a structured dataframe.
                    Pandas helps data manipulation, cleaning, and preprocessing, ensuring that data was ready for analysis.''')
    slt.markdown('''MySQL: With help of SQL to establish a connection to a SQL database, enabling seamless integration of the transformed dataset
                    and the data was efficiently inserted into relevant tables for storage and retrieval.''')
    slt.markdown("Streamlit: Developed an interactive web application using Streamlit, a user-friendly framework for data visualization and analysis.")
    slt.subheader(":red[Coding Done Using:]")
    slt.markdown("Selenium, Python, Pandas, MySQL,mysql-connector-python, Streamlit.")
    slt.subheader(":red[Author:]  Kalpana Velusamy")

if web == "Bus Search":
    states = fetch_state()
    state = slt.selectbox("Lists of States", states,index=None)

    col1,col2=slt.columns(2)
    bus_type =""
    price_range =""

    with col1:
        bus_type = slt.radio("Bus Type", ("sleeper", "semi-sleeper", "others","Any"))
    with col2:
        price_range = slt.radio("Ticket Price", ("50-1000", "1000-2000", "2000 and above","Any"))
    time_range=slt.time_input("Departure Time",value=None)

    routes = fetch_routes(state)
    route=slt.selectbox("List of Routes",routes,index=None)


    df_result = fetch_busses(time_range, state, route, bus_type, price_range)
    slt.dataframe(df_result)
    
