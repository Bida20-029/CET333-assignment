import csv
import pandas as pd
import os
import streamlit as st
import random
from datetime import datetime, timedelta
import geoip2.database
import matplotlib.pyplot as plt

# List of predefined pages on the website
pages = [
    '/homepage.html',
    '/schedule.html',
    '/results.html',
    '/athletes.html',
    '/sports.html',
    '/tickets.html',
    '/venues.html',
    '/news.html',
    '/medal_count.html',
    '/merchandise.html'
]

# Dictionary mapping sports to their respective categories
sports_categories = {
    "Athletics": ["Athletics", "Track and Field"],
    "Ball Sports": ["Basketball", "Football (Soccer)", "Volleyball", "Handball", "Rugby Sevens", "Tennis"],
    "Combat Sports": ["Boxing", "Judo", "Karate", "Taekwondo", "Freestyle Wrestling", "Greco-Roman Wrestling"],
    "Aquatic Sports": ["Swimming", "Diving", "Synchronized Swimming", "Water Polo"],
    "Racquet Sports": ["Badminton", "Table Tennis"],
    "Cycling": ["Cycling", "Road Cycling", "Track Cycling", "Mountain Biking", "BMX Cycling"],
    "Equestrian": ["Equestrian", "Dressage", "Eventing", "Jumping"],
    "Gymnastics": ["Artistic Gymnastics", "Rhythmic Gymnastics", "Trampoline Gymnastics"],
    "Water Sports": ["Canoeing", "Slalom Canoeing", "Sprint Canoeing", "Rowing", "Sailing", "Surfing"],
    "Shooting Sports": ["Shooting"],
    "Winter Sports": ["Biathlon", "Bobsleigh", "Cross-Country Skiing", "Curling", "Figure Skating", "Ice Hockey", "Luge", "Nordic Combined", "Short Track Speed Skating", "Skeleton", "Ski Jumping", "Snowboarding", "Speed Skating", "Curling", "Ice Hockey"]
}

# Function to generate a random IP address
def generate_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

# Function to generate a random timestamp and date
def generate_timestamp():
    start_date = datetime(2024, 4, 1)
    end_date = datetime(2024, 12, 10)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime('%Y-%m-%d %H:%M:%S'), random_date.strftime('%Y-%m-%d')

# Function to generate random request type, URL, and sports category
def generate_request():
    request_types = ['GET', 'POST']
    request_type = random.choice(request_types)
    url = random.choice(pages)  # Assign a random page from predefined pages as URL
    
    # Assign a random sports category as interest
    sport_category = random.choice(list(sports_categories.keys()))
    sport = random.choice(sports_categories[sport_category])
    
    return request_type, url, sport, sport_category

# Function to generate random response status
def generate_status():
    statuses = ['Live', 'Offline']
    return random.choice(statuses)

# Function to categorize countries by region
def categorize_country_by_region(country):
    # Example: Categorize countries into regions (e.g., Europe, Asia, Americas)
    if country in ["United States", "Canada", "Mexico", "Brazil", "Argentina", "Chile"]:
        return "Americas"
    elif country in ["United Kingdom", "Germany", "France", "Italy", "Spain", "Russia"]:
        return "Europe"
    elif country in ["China", "Japan", "South Korea", "India"]:
        return "Asia"
    else:
        return "Other"

# Function to get country of origin from IP address
def get_country(ip_address):
    try:
        with geoip2.database.Reader('GeoLite2-Country.mmdb') as reader:
            response = reader.country(ip_address)
            return response.country.name
    except:
        return "Unknown"

# Generate test data and save to CSV
with open('logs.csv', 'w', newline='') as csvfile:
    fieldnames = ['Timestamp', 'Date', 'IP', 'Country', 'Region', 'RequestType', 'URL', 'Status', 'Interest', 'SportCategory', 'NumberOfUsers', 'Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    users = {}  # Dictionary to track users and their view counts for each category
    for _ in range(5000):  # Generate 1000 log entries
        timestamp, date = generate_timestamp()
        ip = generate_ip()
        country = get_country(ip)
        region = categorize_country_by_region(country)
        request_type, url, sport, sport_category = generate_request()
        stream_status = generate_status()
        
        if sport_category not in users:
            users[sport_category] = {}
        if ip not in users[sport_category]:
            users[sport_category][ip] = {'count': 0, 'views': 0}
        
        users[sport_category][ip]['count'] += 1
        users[sport_category][ip]['views'] += random.randint(1, 5)  # Random views per interaction
        
        writer.writerow({
            'Timestamp': timestamp, 
            'Date': date, 
            'IP': ip, 
            'Country': country, 
            'Region': region, 
            'RequestType': request_type, 
            'URL': url, 
            'Status': stream_status, 
            'Interest': sport, 
            'SportCategory': sport_category, 
            'NumberOfUsers': users[sport_category][ip]['count'], 
            'Views': users[sport_category][ip]['views']
        })


import pandas as pd
import plotly.express as px
import streamlit as st
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Olympics Log File Data", page_icon="bar_chart:",layout="wide")

st.title(" :bar_chart: Olympics Web Server Logs Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df=pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    df = pd.read_csv("logs.csv", encoding = "ISO-8859-1")

total_users = df['NumberOfUsers'].sum()
total_views = df['Views'].sum()
avg_views_per_user = total_views / total_users

st.markdown(
    """
    <style>
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    .metric {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    .metric h3 {
        margin: 0;
        font-size: 1.5em;
        color: #333;
    }
    .metric p {
        margin: 5px 0 0;
        font-size: 1.2em;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True
)

# Display metrics
st.markdown(
    f"""
    <div class="metric-container">
        <div class="metric">
            <h3>Total Users</h3>
            <p>{total_users}</p>
        </div>
        <div class="metric">
            <h3>Total Views</h3>
            <p>{total_views}</p>
        </div>
        <div class="metric">
            <h3>Avg Views per User</h3>
            <p>{avg_views_per_user:.2f}</p>
        </div>
    </div>
    """, unsafe_allow_html=True
)


col1, col2 = st.columns((2))
df["Date"] = pd.to_datetime(df["Date"])

startDate = pd.to_datetime(df["Date"]).min()
endDate = pd.to_datetime(df["Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()


country = st.sidebar.multiselect("Pick your Country", df["Region"].unique(), default=None)
if not country:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(country)]

status = st.sidebar.multiselect("Pick the User's Status", df2["Status"].unique(), default=None)
if not status:
    df3 = df2.copy()
else:
    df3 = df2[df2["Status"].isin(status)]

interest = st.sidebar.multiselect('Pick the interests', df3["Interest"].unique(), default=None)
if not interest:
    df4 = df3.copy()
else:
    df4 = df3[df3["Interest"].isin(interest)]



if not country and not status and not interest:
    filtered_df = df
elif not status and not interest:
    filtered_df = df[df["Country"].isin(country)]
elif not status and not country:
    filtered_df = df[df["Interest"].isin(interest)]
elif status and interest: 
    filtered_df = df3[df["Status"].isin(status) & df3["Interest"].isin(interest)]
elif status and country: 
    filtered_df = df3[df["Status"].isin(status) & df3["Country"].isin(country)]
elif interest and country: 
    filtered_df = df3[df["Interest"].isin(interest) & df3["Country"].isin(country)]
elif country:
    filtered_df = df3[df3["Country"].isin(country)]
else:
    filtered_df = df3[df3["Country"].isin(country) & df3["Interest"].isin(interest) & df3["Status"].isin(status)]

status_df = filtered_df.groupby(by = ["Status"], as_index = False)["NumberOfUsers"].sum()

with col1:
    st.subheader("Live Users")
    fig = px.bar(status_df, x = "NumberOfUsers", y = "Status", text = ['{:,.2f}'.format(x) for x in status_df["NumberOfUsers"]],
                template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.container() 
    st.subheader("Popular Interests")
    fig = px.pie(filtered_df, values="NumberOfUsers", names="SportCategory", hole=0.5)
    fig.update_traces(text=filtered_df["SportCategory"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("ViewData"):
        st.write(status_df.style.background_gradient(cmap="Blues"))
        csv = status_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "logs.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

with cl2:
    with st.expander("ViewData"):
        region = filtered_df.groupby(by = "SportCategory", as_index = False)["NumberOfUsers"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader("Live Users")
    fig = px.bar(filtered_df, x = "NumberOfUsers", y = "Region", text = filtered_df["Region"],
                template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

with chart2:
    st.subheader('Popular URLs')
    fig = px.pie(filtered_df, values = "Views", names = "URL", template = "gridon")
    fig.update_traces(text = df["URL"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

filtered_df["month_year"] = filtered_df["Date"].dt.to_period("M")
st.subheader('Time Series Analysis')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["NumberOfUsers"].sum()).reset_index()
fig2 = px.line(linechart, x = "month_year", y="NumberOfUsers", labels = {"NumberOfUsers": "NumberofUsers"},height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

with st.expander("View Data of TimeSeries:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')

st.subheader("Hierarchical view of Sales using TreeMap")
fig3 = px.treemap(filtered_df, path = ["Region","SportCategory","Interest"], values = "NumberOfUsers",hover_data = ["NumberOfUsers"],
                color = "Interest")
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)
with st.expander("View Data in Table Format"):
    st.subheader("Hierarchical Data of Sales")
    st.dataframe(filtered_df)

import plotly.express as px
df1 = filtered_df.groupby('Country', as_index=False)['NumberOfUsers'].sum()
fig = px.choropleth(
    df1,
    locations='Country',  # use the country names
    locationmode='country names',  # specify that locations are country names
    color='NumberOfUsers',  # data for the color scale
    hover_name='Country',  # column to add to hover information
    color_continuous_scale='Reds',
    projection='natural earth',
    title='Number of Users by Country', 
)
fig.update_layout(
    width=2000,  # specify the width of the figure in pixels
    height=1000  # you can also specify the height if needed
)
st.plotly_chart(fig, use_container_width=True)
with st.expander("View Data in Table Format"):
    st.subheader("User Spread over Map")
    st.dataframe(df1)

csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download All Dashboard Data', data = csv, file_name = "Data.csv",mime = "text/csv")

