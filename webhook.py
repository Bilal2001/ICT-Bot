# import MassegeHandler as ms
import uvicorn
# Importing built-in libraries
import json
import warnings
# Importing dependent libraries
# from enums import SIGNAL_KEY

# Importing third-party libraries
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import pandas as pd
import csv
import os
from datetime import datetime
global app
app = FastAPI()

def log(data):
    # get today's date in YYYY-MM-DD format
    today = datetime.today().strftime('%Y-%m-%d')
    filename = f'{today}.csv'
    # check if the file already exists
    if os.path.isfile(filename):
        # if it does, append data to the file
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            # write your data to the file, for example:
            writer.writerow(list(data.values()))
    else:
        # if it doesn't, create a new file with today's date as its name
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # write headers to the file, for example:
            writer.writerow(list(data.keys()))
            # write your data to the file, for example:
            writer.writerow(list(data.values()))



# def mainWebhook(creds=None, app_config=None):
#     global app
#     app = FastAPI()
#     # sm = ms.SignalManager()
    
#     # sm.set_credentials(creds)
#     # sm.connect_api()
#     uvicorn.run(app=app, host="127.0.0.1", port=5002)


@app.post('/')
def home_page():
    return {"title": "Hello there"}

@app.post('/webhook')
async def webhook(request: Request):
    try:
        # Filtering byte signal into dict
        signal  = await request.body()
        signal = signal.decode('utf-8').replace("'",'"')
        signal = json.loads(signal)
        print(signal, type(signal), sep="\t")
        log(signal)

        # Managing signals
        # if signal[SIGNAL_KEY.PASSPHRASE] == app_config['passphrase']:
        #     sm.manage_signal(signal=signal)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    # with open("credentials.json") as f:
    #     creds = json.load(f)
    #     f.close()
    # with open("app_config.json") as f:
    #     app_config = json.load(f)
    #     f.close()
    # mainWebhook(creds, app_config)

    uvicorn.run(app=app, host="127.0.0.1", port=5002)