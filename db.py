import pandas as pd
import mysql.connector
import numpy as np

details_df=pd.read_csv("bus_details.csv")
details_df["price"]=details_df["price"].str.replace("INR","")
details_df["price"]=details_df["price"].astype(float)
details_df["price"].fillna(0)

details_df["rating"]=details_df["rating"].str.replace("New","")
details_df["rating"]=details_df["rating"].str.strip()
details_df["rating"]=details_df["rating"].str.split().str[0]
details_df["rating"] = pd.to_numeric(details_df["rating"], errors='coerce')
details_df["rating"].fillna(0,inplace=True)

details_df = details_df[details_df["price"] <= 7000]
details_df = details_df.replace({np.nan: None})

path=r"formatted_df.csv"

details_df.to_csv(path,index=False)


conn=mysql.connector.connect(host="localhost", user="root", password="Amyshik@0906",database="red_bus_details")
my_cursor = conn.cursor()
my_cursor.execute("CREATE DATABASE IF NOT EXISTS red_bus_details")

my_cursor.execute('''CREATE TABLE IF NOT EXISTS bus_details(
                  id INT AUTO_INCREMENT PRIMARY KEY,
                  bus_name VARCHAR(255) NOT NULL,
                  bus_type VARCHAR(255) NOT NULL,
                  departure_at VARCHAR(255) NOT NULL,
                  arrival_at VARCHAR(255) NOT NULL,
                  duration VARCHAR(255) NOT NULL,
                  price FLOAT NULL,
                  seats VARCHAR(255) NOT NULL,
                  rating Float NULL,
                  route_link VARCHAR(255) NULL,
                  route_name VARCHAR(255) NULL,
                  state_name VARCHAR(255) NULL
                  )''')
my_cursor.execute("delete from bus_details")

insert_query = '''INSERT INTO bus_details(
                    bus_name,
                    bus_type,
                    departure_at,
                    arrival_at,
                    duration,
                    price,
                    seats,
                    rating,
                    route_name,
                    route_link,
                    state_name)
                  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
data = details_df.values.tolist()

my_cursor.executemany(insert_query, data)

conn.commit()

print("Values inserted successfully")