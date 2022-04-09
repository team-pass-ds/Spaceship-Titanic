import pandas as pd
from scripts import process

# encoder_cols = ['HomePlanet', 'CryoSleep', 'Destination', 'VIP', 'Transported', 'Deck', 'Side', 'LastName']
encoder_cols = ['HomePlanet', 'CryoSleep', 'Destination', 'VIP', 'Deck', 'Side', 'LastName']


df = pd.read_csv('./data/train.csv')
p = process.Preprocess(df)
p.run(encoder_cols)

data = p.data
