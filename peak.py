import pandas as pd
import folium

df = pd.read_csv("data/peaks_with_climbed_flag.csv")

df = df[df["Metres"] >= 800]  # Filter to peaks over 600m

# Create the map centered roughly in Snowdonia
m = folium.Map(location=[53.1, -4.0], zoom_start=10)

# Add markers
for _, row in df.iterrows():
    color = 'green' if row['climbed'] else 'red'
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['Name']} ({row['Metres']} m)",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Save map to HTML
m.save("snowdonia_peaks_map.html")


# import pandas as pd
# import geopandas as gpd
# from shapely.geometry import LineString
# import polyline

# # ---------------------------
# # 1. LOAD YOUR DATA
# # ---------------------------

# df_routes = pd.read_csv("data/activity_data.csv")
# df_peaks = pd.read_csv("data/welsh_mountain_data.csv")

# # Drop rows with no polyline
# df_routes = df_routes.dropna(subset=["map"])

# # ---------------------------
# # 2. CONVERT ROUTES TO LINES
# # ---------------------------

# df_routes["geometry"] = df_routes["map"].apply(
#     lambda x: LineString(polyline.decode(x))
# )

# gdf_routes = gpd.GeoDataFrame(
#     df_routes,
#     geometry="geometry",
#     crs="EPSG:4326"
# )

# # ---------------------------
# # 3. CONVERT PEAKS TO POINTS
# # ---------------------------

# gdf_peaks = gpd.GeoDataFrame(
#     df_peaks,
#     geometry=gpd.points_from_xy(df_peaks.Latitude, df_peaks.Longitude),
#     crs="EPSG:4326"
# )

# # ---------------------------
# # 4. PROJECT TO METERS (UK)
# # ---------------------------

# gdf_routes = gdf_routes.to_crs(epsg=27700)
# gdf_peaks = gdf_peaks.to_crs(epsg=27700)

# # ---------------------------
# # 5. BUFFER PEAKS BY 50m
# # ---------------------------

# gdf_peaks["geometry"] = gdf_peaks.geometry.buffer(50)   # <-- FIXED (was 5)

# # ---------------------------
# # 6. SPATIAL JOIN
# # ---------------------------

# joined = gpd.sjoin(
#     gdf_peaks,
#     gdf_routes,
#     how="left",
#     predicate="intersects"
# )

# # ---------------------------
# # 7. ADD CLIMBED COLUMN (CORRECT WAY)
# # ---------------------------

# gdf_peaks["climbed"] = False

# matched_indexes = joined.loc[joined["index_right"].notna()].index.unique()

# gdf_peaks.loc[matched_indexes, "climbed"] = True

# # ---------------------------
# # 8. SAVE RESULTS
# # ---------------------------

# gdf_peaks.drop(["geometry"], axis=1).to_csv("data/peaks_with_climbed_flag.csv", index=False)

# print("Done.")