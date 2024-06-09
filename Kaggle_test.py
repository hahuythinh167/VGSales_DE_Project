import kaggle 
from kaggle.api.kaggle_api_extended import KaggleApi
import os.path
import pandas as pd

api = KaggleApi()
api.authenticate()
if os.path.isfile('./Dataset/Video_Games_Sales_as_at_22_Dec_2016.csv'):
    print('')
else:
    dataset_kaggle='rush4ratio/video-game-sales-with-ratings'
    api.dataset_download_files(dataset_kaggle, path=f'./Dataset/', unzip=True)
path = './Dataset/Video_Games_Sales_as_at_22_Dec_2016.csv'

pd.set_option('display.max_colwidth', None)
df = pd.read_csv(path)
print(df.head(5))