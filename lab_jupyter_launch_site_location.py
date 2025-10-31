import piplite
await piplite.install(['folium'])
await piplite.install(['pandas'])

import folium
import pandas as pd

# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon

from js import fetch
import io

# Load the data
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
resp = await fetch(URL)
dataset_part_2_csv = io.BytesIO((await resp.arrayBuffer()).to_py())
df = pd.read_csv(dataset_part_2_csv)

# Get unique launch sites with their coordinates
launch_sites = df[['LaunchSite', 'Longitude', 'Latitude']].drop_duplicates()

# Create a map centered around the first launch site
map_center = [launch_sites['Latitude'].iloc[0], launch_sites['Longitude'].iloc[0]]
site_map = folium.Map(location=map_center, zoom_start=4)

# Mark all launch sites on the map
for index, site in launch_sites.iterrows():
    folium.Marker(
        [site['Latitude'], site['Longitude']],
        popup=site['LaunchSite'],
        icon=folium.Icon(color='red', icon='rocket', prefix='fa')
    ).add_to(site_map)

# Display the map
site_map

# Download and read the `spacex_launch_geo.csv`
from js import fetch
import io

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
resp = await fetch(URL)
spacex_csv_file = io.BytesIO((await resp.arrayBuffer()).to_py())
spacex_df=pd.read_csv(spacex_csv_file)

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
launch_sites_df

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)

# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label


# Task 2: Mark the success/failed launches for each site on the map
# Function to assign color based on class (success/failure)
def assign_marker_color(launch_outcome):
    if launch_outcome == 1:
        return 'green'  # Success
    else:
        return 'red'    # Failure

# Add markers for each launch in the dataframe
for index, launch in spacex_df.iterrows():
    folium.CircleMarker(
        location=[launch['Lat'], launch['Long']],
        radius=5,
        color=assign_marker_color(launch['class']),
        fill=True,
        fill_color=assign_marker_color(launch['class']),
        fill_opacity=0.7,
        popup=f"Launch Site: {launch['Launch Site']}<br>Outcome: {'Success' if launch['class'] == 1 else 'Failure'}"
    ).add_to(site_map)

# Display the map
site_map

spacex_df.tail(10)

marker_cluster = MarkerCluster()



# Apply a function to check the value of `class` column
# If class=1, marker_color value will be green
# If class=0, marker_color value will be red
# Create a new column called marker_color
spacex_df['marker_color'] = spacex_df['class'].apply(lambda x: 'green' if x == 1 else 'red')

# Display the last 10 rows to verify
spacex_df.tail(10)

# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)

# for each row in spacex_df data frame
# create a Marker object with its coordinate
# and customize the Marker's icon property to indicate if this launch was successed or failed
for index, record in spacex_df.iterrows():
    # Create and add a Marker cluster to the site map
    marker = folium.Marker(
        location=[record['Lat'], record['Long']],
        icon=folium.Icon(color='white', icon_color=record['marker_color'])
    )
    marker_cluster.add_child(marker)

site_map

# TASK 3: Calculate the distances between a launch site to its proximities
# TASK 3: Calculate the distances between a launch site to its proximities

# First, let's find the coordinates of key proximities for each launch site
# We'll calculate distance to: coastline, railway, highway, city

from math import radians, sin, cos, sqrt, atan2

# Haversine formula to calculate distance between two coordinates
def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert coordinates to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    radius_earth = 6371  # Earth's radius in kilometers
    distance = radius_earth * c
    
    return distance

# Example coordinates for proximities (you'll need to find actual coordinates)
# These are approximate - you should replace with actual coordinates

# For CCAFS SLC-40
coastline_ccafs = [28.561857, -80.577366]  # Approximate coastline near CCAFS
railway_ccafs = [28.562, -80.576]          # Approximate railway
highway_ccafs = [28.563, -80.575]          # Approximate highway
city_ccafs = [28.388, -80.603]             # Cape Canaveral city center

# Calculate distances for CCAFS SLC-40
launch_site_ccafs = [28.561857, -80.577366]

distance_coast = calculate_distance(launch_sites_df['Lat'][0], launch_sites_df['Long'][0], 
                                   coastline_ccafs[0], coastline_ccafs[1])
distance_railway = calculate_distance(launch_sites_df['Lat'][0], launch_sites_df['Long'][0], 
                                     railway_ccafs[0], railway_ccafs[1])
distance_highway = calculate_distance(launch_sites_df['Lat'][0], launch_sites_df['Long'][0], 
                                     highway_ccafs[0], highway_ccafs[1])
distance_city = calculate_distance(launch_sites_df['Lat'][0], launch_sites_df['Long'][0], 
                                  city_ccafs[0], city_ccafs[1])

print(f"CCAFS SLC-40 Proximities:")
print(f"Distance to coastline: {distance_coast:.2f} km")
print(f"Distance to railway: {distance_railway:.2f} km") 
print(f"Distance to highway: {distance_highway:.2f} km")
print(f"Distance to city: {distance_city:.2f} km")

# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)
site_map

from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# find coordinate of the closet coastline
# e.g.,: Lat: 28.56367  Lon: -80.57163
# distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)

# Create and add a folium.Marker on your selected closest coastline point on the map
# Display the distance between coastline point and launch site using the icon property 
# for example
# distance_marker = folium.Marker(
#    coordinate,
#    icon=DivIcon(
#        icon_size=(20,20),
#        icon_anchor=(0,0),
#        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance),
#        )
#    )

# Coordinates for CCAFS SLC-40 launch site
launch_site_lat = 28.563197
launch_site_lon = -80.576820

# Coordinates for closest coastline point (from your mouse position)
coastline_lat = 28.56367
coastline_lon = -80.57163

# Calculate distance to coastline
distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)

# Create and add a marker for the closest coastline point
distance_marker = folium.Marker(
    [coastline_lat, coastline_lon],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
    )
)

# Add the distance marker to the map
site_map.add_child(distance_marker)

# Display the map
site_map

# Create coordinates for the line between launch site and coastline
coordinates = [[launch_site_lat, launch_site_lon], [coastline_lat, coastline_lon]]

# Create a folium.PolyLine object
lines = folium.PolyLine(locations=coordinates, weight=1, color='blue')

# Add the line to the map
site_map.add_child(lines)

# Display the map
site_map

# Create a marker with distance to a closest city, railway, highway, etc.
# Draw a line between the marker to the launch site
# Coordinates for other proximities (replace with actual coordinates from mouse position)
city_lat, city_lon = 28.388, -80.603      # Cape Canaveral city center
railway_lat, railway_lon = 28.572, -80.585 # Nearest railway
highway_lat, highway_lon = 28.563, -80.571 # Nearest highway

# Calculate distances
distance_city = calculate_distance(launch_site_lat, launch_site_lon, city_lat, city_lon)
distance_railway = calculate_distance(launch_site_lat, launch_site_lon, railway_lat, railway_lon)
distance_highway = calculate_distance(launch_site_lat, launch_site_lon, highway_lat, highway_lon)

# Create markers for each proximity with distance labels
city_marker = folium.Marker(
    [city_lat, city_lon],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_city),
    )
)

railway_marker = folium.Marker(
    [railway_lat, railway_lon],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_railway),
    )
)

highway_marker = folium.Marker(
    [highway_lat, highway_lon],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_highway),
    )
)

# Create lines from launch site to each proximity
city_line = folium.PolyLine(
    locations=[[launch_site_lat, launch_site_lon], [city_lat, city_lon]],
    weight=1,
    color='red'
)

railway_line = folium.PolyLine(
    locations=[[launch_site_lat, launch_site_lon], [railway_lat, railway_lon]],
    weight=1,
    color='green'
)

highway_line = folium.PolyLine(
    locations=[[launch_site_lat, launch_site_lon], [highway_lat, highway_lon]],
    weight=1,
    color='orange'
)

# Add all markers and lines to the map
site_map.add_child(city_marker)
site_map.add_child(railway_marker)
site_map.add_child(highway_marker)
site_map.add_child(city_line)
site_map.add_child(railway_line)
site_map.add_child(highway_line)

# Display the map
site_map





