import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


historical_features = pd.DataFrame({
    'Wind_Speed': [10, 15, 12, 25, 20],
    'Payload': [2000, 3500, 1500, 5000, 4500]
})
# The actual delay minutes that occurred for those flights
historical_delays = pd.Series([5, 15, 5, 45, 30])

df = pd.concat([historical_features, historical_delays.rename('Delay')], axis=1)

def predict_flight_delay(df):
    
    X = df[["Wind_Speed", "Payload"]]
    y = df["Delay"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    new_flight = pd.DataFrame({'Wind_Speed': [18], 'Payload': [4000]})
    predicted_delay = model.predict(new_flight)
    error = mean_squared_error(y_test, model.predict(X_test))
    print(f"Predicted delay in(minutes):{round(predicted_delay[0], 2)}")
    print(f"Mean Squared Error: {round(error, 2)}")
    pass
predict_flight_delay(df)
    