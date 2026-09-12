import pandas as pd
import xgboost as xgb
import optuna
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from loguru import logger

def run_ml_pipeline():
    logger.info("--- Booting ML Tuning Engine ---")
    
    # 1. Mock Cargo Data
    # 0 = ON TIME, 1 = DELAYED
    cargo_df = pd.DataFrame({
        "weight_kg": [4000, 9500, 3200, 8900, 1500, 9900, 4100, 8800]*100,
        "distance_km": [500, 1200, 300, 1500, 400, 1600, 450, 1400]*100,
        "delayed": [0, 1, 0, 1, 0, 1, 0, 1]*100 
    })
    
    X = cargo_df[["weight_kg", "distance_km"]]
    y = cargo_df["delayed"]
    
    # 2. Split Data (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Define Optuna Objective
    def objective(trial):
        param_depth = trial.suggest_int("max_depth", 3, 7)
        param_lr = trial.suggest_float("learning_rate", 0.01, 0.3)
        
        model = xgb.XGBClassifier(max_depth=param_depth, learning_rate=param_lr)
        model.fit(X_train, y_train)
        
        preds = model.predict(X_test)
        return accuracy_score(y_test, preds)       

    # 4. Run Optuna Optimization
    logger.info("Starting Hyperparameter Tuning...")
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=5)
    
    logger.success(f"Best parameters found: {study.best_params}")
    
    # 5. Train Final Model & Save
    best_model = xgb.XGBClassifier(**study.best_params)
    best_model.fit(X, y)
    joblib.dump(best_model, "xgboost_delay_model.joblib")
    logger.info("Model saved successfully for production!")

if __name__ == "__main__":
    run_ml_pipeline()