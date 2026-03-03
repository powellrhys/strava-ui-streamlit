

# import pandas as pd
# import folium

# # Load CSV
# df = pd.read_csv("data/welsh_mountain_data.csv")

# # Create base map centered on average coordinates
# map_center = [df["Latitude"].mean(), df["Longitude"].mean()]
# m = folium.Map(location=map_center, zoom_start=10)

# # Add markers
# for _, row in df.iterrows():
#     popup_text = f"""
#     <b>{row['Name']}</b><br>
#     Height: {row['Metres']} m ({row['Feet']} ft)<br>
#     County: {row['County']}
#     """
    
#     folium.Marker(
#         location=[row["Latitude"], row["Longitude"]],
#         popup=popup_text,
#         tooltip=row["Name"]
#     ).add_to(m)

# # Save map
# m.save("mountains_map.html")

# print("Map saved as mountains_map.html")