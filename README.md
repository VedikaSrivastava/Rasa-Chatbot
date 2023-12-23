# University Administration Student Aid Chatbot using RASA

## Set-up to build a chatbot in rasa
- Rasa need specific python version, hence create a enviorment using the following command `conda create -n rasa-env python=3.8`
- now actiavte the enviorment `conda activate rasa-env`
- now install rasa `pip install rasa`
- other requirements have been listed in [requirements.txt](requirements.txt). run `pip install -r requirements.txt`
- a new project can be initiallized using the command `rasa init`, `rasa train` to train the rasa bot, `rasa train nlu` to only train nlu, `rasa run actions` to start the actions server with is esential for database contectivity, `rasa run` to run the bot and `rasa shell` to open the interactive chatbot. `rasa test` to test the bost in different case senerios.

**NOTE:** we have already added the trained model in the repo so to run the bot only enviornment set up is needed then user can do `rasa run actions` followed by `rasa shell`


# commands to run the bot in UI
- `rasa run actions`
- `rasa run --enable-api --cors "*"`: This command runs the Rasa server with API enabled and CORS (Cross-Origin Resource Sharing) allowed from all origins, which is necessary for Streamlit to communicate with Rasa.
- `streamlit run app.py`: Run Streamlit app (Open the URL displayed in terminal to view the Streamlit application)

**NOTE:** we tried deploying the streamlit bot usingb streamlit sharing, however it was always giving some kind of error. you can check the deployement here https://university-chatbot.streamlit.app/  but it doesnt work. So we advise that the UI be run using the 3 commmand mentioned above.


