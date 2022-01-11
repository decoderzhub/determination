import json
import os
import time
import re
import threading
import random
import pandas as pd
import pysftp
import streamlit as st
import geoip2.database
import pydeck as pdk
from stqdm import stqdm
from streamlit_lottie import st_lottie

import hackfacts

pandasdf = pd.DataFrame()
fact_placeholder = st.empty()
attack_placeholder = st.empty()
loading_placeholder = st.empty()
layout_placeholder = st.empty()
auth_log_placeholder = st.empty()
save_name = '/Users/systemd/PycharmProjects/Determination/Data/auth.log'
welcome = True

def retrieve_auth_log():
    os.chdir("/Users/systemd")
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection('149.28.84.56', username='root', private_key='.ssh/id_rsa', cnopts=cnopts) as sftp:
        with sftp.cd('/var/log/'):  # temporarily chdir to public
            sftp.get('auth.log', save_name)  # get a remote file
    print("finished retrieving logs")


# TODO: Goto website for instructions https://regex101.com/r/1Dz72r/1

def create_logs_df():
    global pandasdf, welcome

    pandasdf = pd.DataFrame({'time_stamp': [], 'ssh_id': [], 'action': [], 'username': [], 'ip_address': [], 'port': []})

    regs = r"(?P<time_stamp>\b\w{1,4}. \d{1,2} \d{1,2}:\d{1,2}:\d{1,2}).+\[(?P<ssh_id>\d{1,}(?=\])).*(?P<action>Accepted|Failed|Invalid).+(?P<username>(?<=(for |user)).+(?=\sfrom)).+(?P<ip>(?<=(from\s)).+(?=\sport)).+(?P<port>(?<=(port\s))\d{1,})"

    file = open(save_name)
    lines = file.readlines()

    mplaceholder = st.empty()
    lottie_container = st.empty()
    if welcome:
        mplaceholder.title('🔥🔥🔥 Welcome to Determinator 🔥🔥🔥')
        with open('/Users/systemd/PycharmProjects/Determination/lottie.json', "r") as f:
            data = json.load(f)
            with lottie_container:
                st_lottie(data)

    with loading_placeholder:
        for index in stqdm(range(len(lines)), desc="Loading all things data...😍", mininterval=1):
            m = re.search(regs, lines[index])
            if m:
                time_stamp = m.group('time_stamp')
                ssh_id = m.group('ssh_id')
                action = m.group('action')
                username = m.group('username')
                ip = m.group('ip')
                port = m.group('port')
                with geoip2.database.Reader('/Users/systemd/Downloads/IP_Lookup_City.mmdb') as reader:
                    response = reader.city(ip)
                    pandasdf = pandasdf.append({'time_stamp': time_stamp,
                                    'ssh_id': ssh_id,
                                    'action': action,
                                    'username': username,
                                    'ip_address': ip,
                                    'port': port,
                                    'lon': response.location.longitude,
                                    'lat': response.location.latitude,
                                    "country": response.country.iso_code,
                                    "city": response.city.name
                                    },
                                   ignore_index=True)


    loading_placeholder.empty()

    if welcome:
        mplaceholder.empty()
        lottie_container.empty()
    pandasdf.replace("", float("NaN"), inplace=True)

    pandasdf.dropna(inplace=True)

    pandasdf = pandasdf[pandasdf.ip_address != "24.19.24.56"]
    pandasdf.index = range(len(pandasdf))
    pandasdf.sort_values(by=['time_stamp'], inplace=True, ascending=False)

    #print(pandasdf["action"].value_counts())

    welcome = False

    update_map()


def map(locations, viewstate, zoom, pitch, bearing):
    global pandasdf

    if viewstate == "m1":
        lat_placeholder = 0
        lon_placeholder = 0
    elif viewstate == "m2":
        lat_placeholder = locations[0]
        lon_placeholder = locations[1]
    elif viewstate == "m3":
        lat_placeholder = locations[2]
        lon_placeholder = locations[3]
    elif viewstate == "m4":
        lat_placeholder = locations[4]
        lon_placeholder = locations[5]
    st.write(pdk.Deck(map_style='mapbox://styles/mapbox/dark-v10',
                     initial_view_state=pdk.ViewState(
                         latitude=lat_placeholder,
                         longitude=lon_placeholder,
                         zoom=zoom,
                         pitch=pitch,
                         bearing=bearing
                     ),
                     layers=[
                         pdk.Layer(
                             "HexagonLayer",
                             data=pandasdf,
                             get_position=["lon", "lat"],
                             radius=5000,
                             elevation_scale=20,
                             elevation_range=[0, 10000],
                             pickable=True,
                             extruded=True,
                         ),
                         pdk.Layer(
                             "HeatmapLayer",
                             data=pandasdf.drop_duplicates(),
                             opacity=0.3,
                             get_position='[lon, lat]'
                         ),
                         pdk.Layer(
                             'ScatterplotLayer',
                             data=pandasdf.drop_duplicates(),
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


def update_map():

    global pandasdf

    action = pandasdf["action"].value_counts()
    high3 = pandasdf['ip_address'].value_counts(ascending=False)
    print(high3.keys())

    a = action[0]
    b = action[1]

    global_attacks = a+b

    high = high3[0]
    middle = high3[1]
    low = high3[2]

    high3 = high3.keys()

    hi1 = pandasdf[pandasdf.ip_address == high3[2]]

    # print(hi1.iloc[0])
    # print(high3[2])
    #
    # print(*high3)

    locations = []

    for x in range(0, 3):
        with geoip2.database.Reader('/Users/systemd/Downloads/IP_Lookup_City.mmdb') as reader:
            response = reader.city(high3[x])

            locations.append(response.location.latitude)

            locations.append(response.location.longitude)

    with layout_placeholder:

        m1, m2, m3, m4 = st.columns((2, 1, 1, 1))

        with m1:
            zoom, pitch, bearing = 0, 0, 0
            st.write('**Global Attacks',str(global_attacks),'**')
            map(None, "m1", zoom, pitch, bearing)
        with m2:
            zoom, pitch, bearing = 6, 55, 60
            st.write('**1st',str(high),'Attacks**')
            map(locations, "m2", zoom, pitch, bearing)
        with m3:
            zoom, pitch, bearing = 6, 55, 60
            st.write('**2nd',str(middle),'Attacks**')
            map(locations, "m3", zoom, pitch, bearing)
        with m4:
            zoom, pitch, bearing = 6, 55, 60
            st.write('**3rd',str(low),'Attacks**')
            map(locations, "m4",zoom, pitch, bearing)

        update_auth_log()


def update_auth_log():
    global pandasdf
    auth_log_placeholder\
        .dataframe(data=pandasdf.assign(hack='')
                   .set_index('hack')
                   .head(50))
    update_attacked()


def update_attacked():
    global pandasdf
    action = pandasdf["action"].value_counts()
    a = str(action[0])
    b = str(action[1])
    failed = "🔥"+a+"🔥"
    invalid = "🔥"+b+"🔥"
    if len(action) > 1:
        attack_placeholder.write(pd.DataFrame({
                'Failed_Attacks': [failed],
                'Invalid_Attacks': [invalid],
        }).assign(hack="").set_index('hack'))


def heartbeat(args):

    while True:
        retrieve_auth_log()
        create_logs_df()
        time.sleep(args)

def display_facts(args):
    while True:
        with fact_placeholder:
            fact_placeholder.title(random.choice(hackfacts.facts))
        time.sleep(args)


if __name__ == "__main__":
    # retrieve_auth_log()
    # update_attacked()
    init = threading.Thread(target=heartbeat, args=(120,), daemon=True)
    facts = threading.Thread(target=display_facts, args=(60,), daemon=True)
    st.report_thread.add_report_ctx(init)
    st.report_thread.add_report_ctx(facts)
    init.start()
    facts.start()
    init.join()
    facts.join()
    update_map()



