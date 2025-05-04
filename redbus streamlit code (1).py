#example

import streamlit as st
import pandas as pd
import pymysql
import streamlit as st
from PIL import Image

# Connect to MySQL
mydb = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="bike",
    database="redbus",
)

mycursor = mydb.cursor()

# Fetch data from the database
mycursor.execute("SELECT * FROM busdatas")
data = mycursor.fetchall()
columns = [desc[0] for desc in mycursor.description]
table = pd.DataFrame(data, columns=columns)



# Clean the data by converting star_rating, price, and seats_available to numeric types
table["star_rating"] = pd.to_numeric(table["star_rating"], errors='coerce').round(1)# Convert to numeric, NaNs for errors
table["price"] = pd.to_numeric(table["price"], errors='coerce').round(0).astype("Int64")  # Convert to numeric, NaNs for errors
table["seats_available"] = pd.to_numeric(table["seats_available"], errors='coerce')  # Convert to numeric, NaNs for errors


#24hours time to normal time
table["departing_time"] = table["departing_time"].apply(
    lambda x: pd.to_datetime(x, format="%H:%M").strftime("%I:%M %p") if isinstance(x, str) else x)


#Round the rating value
table["star_rating_display"] = table["star_rating"].apply(lambda x: f"{x:.1f}" if pd.notnull(x) else "")


# Get unique states
statelist = table["state"].unique().tolist()
statelist = ["Choose your state"] + statelist


# Load and display an image from a local file
image = Image.open("C:/Users/dhars/Downloads/buss.jpg")  # Fixed file path using raw string literal
st.image(image, use_column_width=True)
# Display the caption in black color using Markdown
st.markdown('<h2 style="color:black; font-size:20px;">WELCOME 🤝</h2>', unsafe_allow_html=True)


# Streamlit UI
st.markdown("<h1 style='color: red;'>Redbus Data Scraping Project</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: black;'>Check the buses availability here!</h3>", unsafe_allow_html=True)

# State selection
selected_state = st.selectbox("States", statelist)

if selected_state != "Choose your state":
    # Filter routes based on selected state
    routes = table[table["state"] == selected_state]["route_name"].unique().tolist()
    route_selected = st.selectbox("Routes", ["Choose your desired route"] + routes)


 # Sidebar for filters
    st.sidebar.markdown("<h3 style='color: maroon;'>Filter star rating</h3>", unsafe_allow_html=True)
    rating = st.sidebar.radio(
        "Rating",
        options=[5, 4, 3, 2, 1],
        format_func=lambda x: "⭐" * x,
        horizontal=True
    )

    st.sidebar.markdown("<h3 style='color: maroon;'>Filter ticket fare</h3>", unsafe_allow_html=True)
    max_price = st.sidebar.slider("Price in INR", 100, 10000, 100, 100)

    st.sidebar.markdown("<h3 style='color: maroon;'>Select tickets count</h3>", unsafe_allow_html=True)
    seats = st.sidebar.number_input("seats", min_value=1, max_value=50)


    if max_price > 100:
        # Apply filters based on user selections
        buses = table[
            (table["route_name"] == route_selected) &
            (table["star_rating"] >= rating) &
            (table["price"] <= max_price) &
            (table["seats_available"] >= seats)
        ]["busname"].tolist()

        # Bus selection
        bus_selected = st.radio("Available buses", buses)


        if bus_selected:
            if st.button(f"{bus_selected} bus details"):
                # Display bus details
                bus_details = table[
                    (table["state"] == selected_state) &
                    (table["route_name"] == route_selected) &
                    (table["busname"] == bus_selected)
                ][["bustype", "departing_time", "duration", "star_rating_display", "price","seats_available"]]
                
                
                st.table(bus_details)









