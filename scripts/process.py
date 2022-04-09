import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression

import seaborn as sns
import matplotlib.pyplot as plt

class Preprocess:
    
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.encoders = None
        self.data = None
    
    # Break PassengerId into GroupId and PassengerId
    def process_PassengerId(self) -> None:
        gids, pids = [], []
        for p in self.df.PassengerId.tolist():
            t = p.split('_')
            gids.append(t[0])
            pids.append(t[1])
        self.df['GroupId'] = gids
        self.df['PassengerId'] = pids
    
    # Breaking Cabin into deck, num & side
    def process_Cabin(self) -> None:
        decks, nums, sides = [], [], []
        lists = [decks, nums, sides]
        for cabin in self.df.Cabin.tolist():
            if pd.isna(cabin):
                for l in lists:
                    l.append(np.nan)
            else:
                x = cabin.split('/')
                for i, l in enumerate(lists):
                    l.append(x[i])
        self.df['Deck'] = decks
        self.df['Num'] = nums
        self.df['Side'] = sides
        # Typecasting num values to int whereever possbile, else keeping nan
        self.df['Num'] = self.df.Num.apply(lambda x: int(x) if not pd.isna(x) else np.nan)
    
    # Feature engineering lastname
    @staticmethod
    def get_last_name(name: str) -> str:
        if pd.isna(name): return ''
        else: return name.split(' ')[1]
    
    @staticmethod
    def get_encoder_dictionary(df: pd.DataFrame, encode_cols: List[str], **kwargs) -> Dict[str, LabelEncoder]:
        encoders: Dict[str, LabelEncoder] = {}
        
        # For every column we're fitting the encoder
        # with all non null values and save it in the
        # encoders dictionary with the key `column`
        for column in encode_cols:
            l = LabelEncoder(**kwargs)
            non_null_values: List[Any] = df[~pd.isna(df[column])][column].tolist()
            l.fit(non_null_values)
            encoders[column] = l
        
        return encoders
    
    @staticmethod
    def impute_with_model(
        df: pd.DataFrame,
        target: str,
        encoders: Dict[str, LabelEncoder],
        type_: str = 'C'
    ) -> pd.DataFrame:

        # Columns to exclude
        exclude_cols = ['PassengerId', 'Cabin', 'Name', 'Transported']
        
        # Exit condition
        if df[pd.isna(df[target])].shape[0] == 0:
            return df
        
        model = DecisionTreeClassifier() if type_ == 'C' else LinearRegression()
        # Columns that're to be used for this model
        include_cols = [x for x in df.columns if x not in exclude_cols]
        
        # Making a copy of the dataframe
        temp = df[include_cols].copy(deep=True)
        temp.dropna(inplace=True)
        
        for c in temp.columns:
            if c in encoders:
                temp[c] = encoders[c].transform(temp[c])
        
        X, y = (temp[[x for x in df.columns if x not in exclude_cols + [target]]], 
                temp[target])

        # Final training
        model.fit(X, y)
        # Processing the entire dataframe for prediction
        X_new = df[pd.isna(df[target])][X.columns].dropna()
        
        # Encoding values for prediction
        for column, encoder in encoders.items():
            if column in X_new.columns:
                X_new[column] = encoder.transform(X_new[column])
        # Making predictions
        preds = model.predict(X_new)
        labels = encoders[target].inverse_transform(preds) if (
            type_ == 'C'
        ) else df[target].tolist()
        # Adding the predictions to respective columns
        idx_preds_mapping: List[Tuple[int, str]] = list(zip(X_new.index.tolist(), labels))
        for idx, p in idx_preds_mapping:
            df.loc[df.index==idx, target] = p
        # For the rest of the missing attributes we're imputing with mode or 
        # median depending on the type of var
        x = df[target].mode().iloc[0] if type_ == 'C' else df[target].median()
        df.loc[pd.isna(df[target]), target] = x
        return df
    
    def handle_missing_values(self, encoder_cols) -> None:
        # Which columns to encode??
        
        self.encoders = Preprocess.get_encoder_dictionary(self.df, encoder_cols)
        
        # Columns that we'd have to impute
        cols_to_impute = [
            ('HomePlanet', 'C'), ('CryoSleep', 'C'), ('Destination', 'C'),
            ('Age', 'R'), ('VIP', 'C'), ('RoomService', 'R'), ('FoodCourt', 'R'), 
            ('ShoppingMall', 'R'), ('Spa', 'R'), ('VRDeck', 'R')
        ]
        
        for col, type_ in cols_to_impute:
            self.df = Preprocess.impute_with_model(
                self.df, col, self.encoders, type_
            )
    
    def create_TotalSpent(self) -> None:
        self.df['TotalSpent'] = self.df[
            ['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
        ].apply(lambda x: sum(x), axis=1)
    
    def final_imputation(self) -> None:
        self.df.loc[pd.isna(self.df.Deck), 'Deck'] = self.df.Deck.mode().iloc[0]
        self.df.loc[pd.isna(self.df.Num), 'Num'] = self.df.Num.mode().iloc[0]
        self.df.loc[pd.isna(self.df.Side), 'Side'] = self.df.Side.mode().iloc[0]

    def run(self, encoder_cols: List[str]) -> None:
        
        self.process_PassengerId()
        self.process_Cabin()
        self.df['LastName'] = self.df.Name.apply(lambda x: Preprocess.get_last_name(x))
        self.df.GroupId = self.df.GroupId.apply(lambda x: int(x))
        self.handle_missing_values(encoder_cols)
        self.create_TotalSpent()
        self.final_imputation()
        
        self.df.PassengerId = self.df.PassengerId.apply(lambda x: int(x))
        
        # Creating numeric df
        self.data = self.df.copy(deep=True)
        for column, encoder in self.encoders.items():
            self.data[column] = encoder.transform(self.data[column])
        