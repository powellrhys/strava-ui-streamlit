# strava-api

The following reposiotry contains iteration 1.0 of leveraging the [strava-api](https://www.bing.com/search?q=strava+api&cvid=a5a113b1252641b58bd7edc0c46fb8e3&aqs=edge..69i57j0j69i59j0l3j69i60l3.3591j0j1&pglt=43&FORM=ANNTA1&PC=DCTS) to map athlete data. 

Visuals were generated using [folium](https://python-visualization.github.io/folium/) and rendered using [streamlit](https://streamlit.io/).

Iteration 1.0 currently does not support container deployment and therefore can only be run locally at this point. The streamlit frontend may be initialised via the following command:

`streamlit run Home.py`

Upon running the command, navigate to port 8501 within your browser : 

`https://http://localhost:8501/`. 

Once on the landing page, enter an athlete's API `client_id` and `client_secret` before clicking the log in button. Information on how to retrieve these values can be found [here](https://developers.strava.com/docs/getting-started/).

Upon browser re-direction, login to your strava account and copy and paste the `code` paramater from the re-directed url (this is your `access_token`). 

Proceed to enter this value back into the landing page to retrieve your athlete's data. 

Once the data has been downloaded, navigate to the second tab to view your athlete's strava heatmap. 
