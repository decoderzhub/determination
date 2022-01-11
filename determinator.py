import main
import streamlit as st
import pydeck as pdk

h1, h2 = st.columns(2)
mp1, mp2 = st.columns(2)

with h1:
    st.title("Determinator")
    st.subheader("1st SFG Cyber Lab")

with h2:
    h2.write("facts")
    #main.init_fact()

with mp1:
    map_placeholder = st.empty()
    mp1.write("map1")
    map_placeholder.pydeck_chart(
        pdk.Deck(map_style='mapbox://styles/mapbox/dark-v10',
                 layers=[
                     pdk.Layer(
                         "HeatmapLayer",
                         data=None,
                         opacity=0.3,
                         get_position=['lon', 'lat']
                     ),
                     pdk.Layer(
                         'ScatterplotLayer',
                         data=None,
                         get_position='[lon, lat]',
                         pickable=True,
                         opacity=0.8,
                         stroked=True,
                         filled=True,
                         radius_scale=6,
                         radius_min_pixels=5,
                         radius_max_pixels=100,
                         line_width_min_pixels=1,
                         get_fill_color=[255, 215, 0],
                         get_line_color=[0, 0, 0]
                     ),
                 ],
                 tooltip={"html": "<b>Username: </b> {username} <br /> "
                                  "<b>IP: </b> {ip_address} <br /> "
                                  "<b>Port: </b> {port} <br /> "
                                  "<b>Action: </b> {action} <br /> "
                                  "<b>Lon: </b> {lon} <br /> "
                                  "<b>Lat: </b>{lat} <br /> "
                                  "<b>City: </b>{city} <br /> "
                                  "<b>Country: </b>{country}"}
                 )
    )

with mp2:
    map2_placeholder = st.empty()
    mp2.write("map2")
    map2_placeholder.pydeck_chart(
        pdk.Deck(map_style='mapbox://styles/mapbox/dark-v10',
                 layers=[
                     pdk.Layer(
                         "HeatmapLayer",
                         data=None,
                         opacity=0.3,
                         get_position=['lon', 'lat']
                     ),
                     pdk.Layer(
                         'ScatterplotLayer',
                         data=None,
                         get_position='[lon, lat]',
                         pickable=True,
                         opacity=0.8,
                         stroked=True,
                         filled=True,
                         radius_scale=6,
                         radius_min_pixels=5,
                         radius_max_pixels=100,
                         line_width_min_pixels=1,
                         get_fill_color=[255, 215, 0],
                         get_line_color=[0, 0, 0]
                     ),
                 ],
                 tooltip={"html": "<b>Username: </b> {username} <br /> "
                                  "<b>IP: </b> {ip_address} <br /> "
                                  "<b>Port: </b> {port} <br /> "
                                  "<b>Action: </b> {action} <br /> "
                                  "<b>Lon: </b> {lon} <br /> "
                                  "<b>Lat: </b>{lat} <br /> "
                                  "<b>City: </b>{city} <br /> "
                                  "<b>Country: </b>{country}"}
                 )
    )

