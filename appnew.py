# importing libraries
import pandas as pd
import mysql.connector
import streamlit as slt
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image

def fetch_details(query):
    conn = mysql.connector.connect(host="localhost", user="root", password="Amyshik@0906", database="red_bus_details")
    my_cursor = conn.cursor()
    my_cursor.execute(query)
    data = my_cursor.fetchall()
    conn.close()

    return data

def fetch_busses(time_range, state, route, bus_type, price_min,price_max):
    #if price_range == "50-1000":
   #     price_min, price_max = 50, 1000
    #elif price_range == "1000-2000":
    #    price_min, price_max = 1000, 2000
    #elif price_range == "Any":
    #    price_min, price_max = 50, 100000
    #else:
    #    price_min, price_max = 2000, 100000

    if bus_type == "sleeper":
        bus_type_condition = "bus_type LIKE '%Sleeper%'"
    elif bus_type == "semi-sleeper":
        bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
    elif bus_type == "Any":
        bus_type_condition = "bus_type IS NOT NULL"
    else:
        bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"
    if time_range =="Before 6 AM":
        time_range_condition = "departure_at<='06:00'"
    elif time_range == "6 AM to 12 PM":
        time_range_condition = "departure_at between '06:00' and '12:00'"
    elif time_range == "12 PM to 6 PM":
        time_range_condition = "departure_at between '12:00' and '18:00'"
    elif time_range == "After 6 PM":
        time_range_condition = "departure_at>='18:00'"
    else:
        time_range_condition = "departure_at>='00:00'"
    if rating_input == "4 ⭐ And Above":
        rating_condition = "Rating>=4"
    elif rating_input == "3 ⭐ And Above":
        rating_condition = "Rating>=3"
    else:
        rating_condition = "Rating IS NOT NULL"
    query = f'''
            SELECT 
             bus_name, bus_type, departure_at, arrival_at, duration,
            price, seats, rating
               FROM bus_details
            WHERE price BETWEEN {price_min} AND {price_max}
            AND route_name = "{route}"
            AND state_name = "{state}"
            AND {bus_type_condition} AND {time_range_condition} AND {rating_condition}
            ORDER BY price and departure_at DESC
        '''
    data = fetch_details(query)
    
    df = pd.DataFrame(data, columns=[
             "Travels Name", "Bus Type", "Departure Time", "Arrival Time", "Duration",
            "Price", "Seats Available", "Rating"
        ])
    df["Seats Available"]=df["Seats Available"].str.replace(" Seats available","")
    
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

slt.set_page_config("RedBus - Online Bus Search",layout="wide")

slt.title(":red[**RedBus**] :rainbow[**Online Bus Search**]")

#original_title = '<p style="font-family:Courier; color:rainbow; font-size: 60px;">RedBus</p>'
#slt.title(original_title)

def load_css():
    with open("streamlitCSS.css") as f:
        slt.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


bus_type =""
price_range =""
rating_input = ""

image = Image.open("red_bus1.jpg")
new_image = image.resize((700, 200))
slt.image(new_image)



# Use the custom label with the select box

slt.sidebar.title("🔍 Search Your Bus")

states = fetch_state()

state = slt.sidebar.selectbox("**SELECT STATE**:red[*]",states,index=None,placeholder='**Select the state name..**')


routes = fetch_routes(state)

route=slt.sidebar.selectbox("**SELECT ROUTE**:red[*]",routes,index=None,placeholder='**Select the route..**')


price_min,price_max=slt.sidebar.slider("**TICKET PRICE RANGE**:red[*]", min_value=0, max_value=10000, value=(0,1000),label_visibility="visible")

bus_type = slt.sidebar.selectbox("**SELECT BUS TYPE** ***optional***", ("Any","Sleeper", "Semi-sleeper", "Others"))

rating_input = slt.sidebar.selectbox("**SELECT BUS RATING** ***optional***", ("4 ⭐ And Above", "3 ⭐ And Above")
                                     ,index=None,placeholder='Select rating..')

time_range = slt.sidebar.radio("**DEPARTURE TIME**", ("Any","Before 6 AM", "6 AM to 12 PM", "12 PM to 6 PM","After 6 PM"))



df_result = fetch_busses(time_range, state, route, bus_type, price_min,price_max)

slt.dataframe(df_result,
              column_config={
        "Travels Name": slt.column_config.Column("Travels Name", width="small"),
        "Bus Type": slt.column_config.Column("Bus Type", width="medium"),
        "Departure Time": slt.column_config.Column("Departure Time", width="small"),
        "Arrival Time": slt.column_config.Column("Arrival Time", width="small"),
        "Duration": slt.column_config.Column("Duration", width="small"),
        "Price": slt.column_config.Column("Price(INR)", width="small"),
        "Seats Available": slt.column_config.Column("Seats Available", width="small"),
        "Rating": slt.column_config.Column("Rating", width="small")
        },hide_index=True,use_container_width=True
              )

footer = """<div class='footer'><p>Credits: Kalpna Velusamy</p></div>"""
slt.markdown(footer, unsafe_allow_html=True)

    
