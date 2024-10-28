from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import time
# importing libraries
import pandas as pd

base_url = "https://www.redbus.in/"
route_pages = 2

state_transports = [
        {
            "name":"WBTC-West Bengal",
            "end_point":"online-booking/wbtc-ctc/?utm_source=rtchometile"
        }
 ]

# #10 states links
# state_links=[
#       {
#           "name":"KSRTC-KERALA",
#          "end_point":"online-booking/ksrtc-kerala/?utm_source=rtchometile"
#        },
#        {
#            "name":"APSRTC-Andhra",
#            "end_point":"online-booking/apsrtc/?utm_source=rtchometile"
#        },
#        {
#            "name":"TSRTC-Telangana",
#            "end_point":"online-booking/tsrtc/?utm_source=rtchometile"
#        },
#        {
#            "name":"KTCL-Goa",
#            "end_point":"online-booking/ktcl/?utm_source=rtchometile"
#        },
#        {
#            "name":"RSTC-Rajasthan",
#            "end_point":"online-booking/rsrtc/?utm_source=rtchometile"
#        },
#        {
#            "name":"SBSTC-South Bengal",
#            "end_point":"online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile"
#        },
#        {
#            "name":"HRTC-Himachal",
#            "end_point":"online-booking/hrtc/?utm_source=rtchometile"
#        },
#        {
#            "name":"ASTC-Assam",
#            "end_point":"online-booking/astc/?utm_source=rtchometile"
#        },
#        {
#            "name":"UPSTC-Uttar Pradesh",
#            "end_point":"online-booking/uttar-pradesh-state-road-transport-corporation-upsrtc/?utm_source=rtchometile"
#        },
#        {
#            "name":"WBTC-West Bengal",
#            "end_point":"online-booking/wbtc-ctc/?utm_source=rtchometile"
#        }
#
#    ]
driver=webdriver.Chrome()

driver.get(base_url)
time.sleep(3)
driver.maximize_window()
wait = WebDriverWait(driver, 20)

state_routes = pd.DataFrame();
#fetch routes for the chosen state
def fetch_routes(item):
    driver.get(base_url + item['end_point']) #launch the url for the state
    time.sleep(3)
    route_links=[]
    route_names=[]
    route_element_path = "//a[@class='route']"

    for i in range(1, route_pages):
        paths=driver.find_elements(By.XPATH, route_element_path)

        for route_link in paths:
            d = route_link.get_attribute("href") #fetch the route links from the elment found 
            route_links.append(d)

        for route_name in paths:
            route_names.append(route_name.text) #find the route names from the elements found

        try:
            pagination = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]'))
            )
            #find the next page button
            next_button = pagination.find_element(
                By.XPATH, f'//div[contains(@class, "DC_117_pageTabs") and not(contains(@class, "DC_117_pageActive")) and text()={i + 1}]'
            )
            
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            time.sleep(2)
            #click next page button if found
            try:
                next_button.click()
            except ElementClickInterceptedException: 
                driver.execute_script("arguments[0].click();", next_button)

        except (NoSuchElementException, TimeoutException):
            print(f"No more pages to paginate at step {i}") #throw excpetion if no next page available
            break
    #create data frame and save the route name and links
    route_df=pd.DataFrame({
        "route_name":route_names,
        "route_link":route_links,
    })
    #create a column for the state name
    route_df['state_name'] = item['name']
    return route_df

for item in state_transports:
    route_df = fetch_routes(item)
    state_routes = pd.concat([state_routes, route_df], ignore_index=True)

#save the collected route details into csv file
path=r"state_routes.csv"
state_routes.to_csv(path,index=False)


#fetch bus details of all the routes for the chosen state 

def fetch_bus_details(name, link, state):
    bus_names = []
    bus_types = []
    departure_at = []
    arrival_at = []
    ratings = []
    durations = []
    prices = []
    seats = []

    driver.get(link)
    time.sleep(6)

    #Click view bus button
    try:
        clicks = driver.find_element(By.XPATH, "//div[@class='button']")
        clicks.click()
    except:
        pass

    time.sleep(2)
    #scroll down 
    scrolling = True
    while scrolling:
        old_page_source = driver.page_source

        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()

        time.sleep(5)


        new_page_source = driver.page_source

        if new_page_source == old_page_source:
            scrolling = False
    #Capture bus details by xpath 
    bus_name_paths = driver.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
    bus_type_path = driver.find_elements(By.XPATH, "//div[@class='bus-type f-12 m-top-16 l-color evBus']")
    departure_at_path = driver.find_elements(By.XPATH, "//*[@class='dp-time f-19 d-color f-bold']")
    arrival_at_path = driver.find_elements(By.XPATH, "//*[@class='bp-time f-19 d-color disp-Inline']")
    duration_path = driver.find_elements(By.XPATH, "//*[@class='dur l-color lh-24']")
    try:
        rating_path= driver.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
    except:
        rating_path = []

    price_path = driver.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seat_path = driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")
    #Append each bus details to each list that belongs to the detail
    for item in bus_name_paths:
        bus_names.append(item.text)
    for item in bus_type_path:
        bus_types.append(item.text)
    for item in departure_at_path:
        departure_at.append(item.text)
    for item in arrival_at_path:
        arrival_at.append(item.text)
    for item in duration_path:
        durations.append(item.text)
    for item in rating_path:
        ratings.append(item.text)
    for item in price_path:
        prices.append(item.text)
    for item in seat_path:
        seats.append(item.text)


    data = {
        'bus_name': bus_names,
        'bus_type': bus_types,
        'departure_at': departure_at,
        'arrival_at': arrival_at,
        'duration': durations,
        'price': prices,
        "seats":seats,
        "rating":ratings
    }
    #save the details in a data frame along with the route name,link and state name
    details_df = pd.DataFrame(data)

    details_df['route_name'] = name
    details_df['route_link'] = link
    details_df['state_name'] = state
    return details_df #return the data frame


bus_details = pd.DataFrame();
for i,r in state_routes.head(20).iterrows():
    link=r["route_link"]
    name=r["route_name"]
    state=r["state_name"]

    details_df = fetch_bus_details(name, link, state)
    bus_details = pd.concat([bus_details, details_df], ignore_index=True) #concat the details of each route name in to the dataframe

bus_details_path=r"bus_details.csv"
bus_data_final = bus_details.dropna() #remove the empty rows if any
bus_data_final.to_csv(bus_details_path,index=False) # convert the bus details data frame with all routes and details to csv file

