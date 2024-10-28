
# RedBus Webscrapping with Selenium using Streamlit

The "Redbus Data Scraping and Filtering with Streamlit Application" aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry.

# Code Details

There are 3 coding files attached here:

- scrapper.py
- db.py
- appnew.py

# scrapper.py

 The code file named scrapper.py handles the web scrapping from redbu website.
 - Selenium libraries imported and functions used from Selenium
 - driver function used to drive the web browser 
 - find_elements used to fetch the details from the browser by their xpath, class or id etc.
 - wait.until function used to make the execution wait until the required element present one the browser
 - actionschains used to perform the scroll down keys
 - pandas was imported and used here to handle the data frame

 # db.py
 - db.py handles the db connection to create the database and table to for the bus details
 - Bus details and route details captured from scrapper.py are inserted by the db.py
 - python mysql connector library used to handle the db connection

 # appnew.py
 - app.py uses streamlit library to create interactive web app
 - Functions defined to connect to DB and fetch bus details based on the options selected (like state, route , bus type and so)

# Execution Steps
- Step1 : execute scrapper.py
    `python scrapper.py`
- Step2 : execute db.py
    `python db.py`
- Step3 : execute app.y
    `streamlit run appnew.py`

Use the interactive web app to see the bus details.
