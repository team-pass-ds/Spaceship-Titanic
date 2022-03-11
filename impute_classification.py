import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from typing import Dict, List, Tuple

def impute_with_classification(
    df: pd.DataFrame,
    target_attribute: str,
    exclude_cols: List[str],
    encoders: Dict[str, LabelEncoder],
    test: bool = True
) -> pd.DataFrame:
    
    # Exit condition
    if df[pd.isna(df[target_attribute])].shape[0] == 0:
        return df
    
    model = DecisionTreeClassifier()
    # Columns that're to be used for this model
    include_cols = [x for x in df.columns if x not in exclude_cols]
    print(include_cols)
    
    # Making a copy of the dataframe
    temp = df[include_cols].copy(deep=True)
    temp.dropna(inplace=True)
    
    for c in temp.columns:
        if c in encoders:
            temp[c] = encoders[c].transform(temp[c])
    
    X, y = (temp[[x for x in df.columns if x not in exclude_cols + [target_attribute]]], 
            temp[target_attribute])

    if test:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
        model.fit(X_train, y_train)
        # Scores n stuff
        preds = model.predict(X_test)
        plt.figure(figsize=(7, 5))
        sns.heatmap(confusion_matrix(y_test, preds), annot=True, fmt='.0f')
        plt.show()
        print('\t\tCLASSIFICATION REPORT OF DTREE!\n', '\t\t', '~'*40)
        print(classification_report(y_test, preds))
    
    # Final training
    model.fit(X, y)
    # Processing the dataframe for prediction
    X_new = df[pd.isna(df[target_attribute])]
    # Selecting only those rows
    X_new = X_new[X.columns]
    old_shape = X_new.shape[0]
    X_new.dropna(inplace=True)
    print('Had to drop {} rows'.format(old_shape - X_new.shape[0]))
    
    # Encoding values for prediction
    for column, encoder in encoders.items():
        if column in X_new.columns:
            X_new[column] = encoder.transform(X_new[column])
    predictions = model.predict(X_new)
    labels = encoders[target_attribute].inverse_transform(predictions)
    index_prediction_mapping: List[Tuple[int, str]] = list(zip(X_new.index.tolist(), labels))
    for idx, p in index_prediction_mapping:
        df.loc[df.index==idx, target_attribute] = p
    
    # For the rest of the missing attributes we're imputing with mode
    df.loc[pd.isna(df[target_attribute]), target_attribute] = df[target_attribute].mode().iloc[0]
    return df