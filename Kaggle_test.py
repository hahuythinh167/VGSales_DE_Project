import kaggle 
from kaggle.api.kaggle_api_extended import KaggleApi
import os.path

api = KaggleApi()
api.authenticate()
if os.path.isfile('./Dataset/Video_Games_Sales_as_at_22_Dec_2016.csv'):
    print(1)
else:
    dataset_kaggle='rush4ratio/video-game-sales-with-ratings'
    api.dataset_download_files(dataset_kaggle, path=f'./Dataset/', unzip=True)