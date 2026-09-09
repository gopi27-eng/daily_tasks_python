import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
# 1. Import LogisticRegression and accuracy_score here


# Historical Data: Wind_Speed, Payload, and a binary category (1 = Delayed, 0 = On-Time)
historical_features = pd.DataFrame({
    'Wind_Speed': [10, 25, 12, 30, 15, 28, 8, 22],
    'Payload': [2000, 5000, 1500, 5500, 3500, 4800, 1200, 4500]
})
historical_status = pd.Series([0, 1, 0, 1, 0, 1, 0, 1], name='Status')
df = pd.concat([historical_features, historical_status], axis=1)

def build_classifier():
    X_train, X_test, y_train, y_test = train_test_split(
        historical_features, historical_status, test_size=0.25, random_state=42
    )
    
    # 2. Initialize LogisticRegression
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    
    # 3. Train the model
    # 
    
    # 4. Predict on X_test
    y_pred = model.predict(X_test)
    
    # 5. Calculate and print accuracy_score(y_test, predictions)
    accuracy = accuracy_score(y_test,y_pred)
    print(f"Accuracy of the model is: {accuracy}")
    # ...
    
    pass

build_classifier()