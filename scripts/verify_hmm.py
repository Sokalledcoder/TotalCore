import requests
import json

BASE_URL = "http://localhost:8000/api/hmm"

def verify_hmm():
    # 1. Train
    print("Training model...")
    # Note: We assume the server is running. 
    # Since I can't strictly rely on the server running in this environment, 
    # I will import the router logic directly if possible, or just use the service classes.
    # But for a true integration test, I should use the service classes directly.
    
    from app.services.hmm_engine import HMMModel
    from app.db import db
    
    # Fetch data from DB (populated in previous step)
    df = db.get_market_data("binance", "BTC/USDT", "15m")
    if df.empty:
        print("FAILURE: No data in DB to train on.")
        return

    print(f"Training on {len(df)} rows...")
    model = HMMModel(n_components=3)
    stats = model.train(df)
    
    print("Training Stats:")
    print(json.dumps(stats, indent=2))
    
    # 2. Predict
    print("Predicting...")
    probs = model.predict_proba(df)
    states = model.predict(df)
    
    print(f"Last State: {states[-1]}")
    print(f"Last Probs: {probs[-1]}")
    
    if abs(sum(probs[-1]) - 1.0) > 1e-5:
        print("FAILURE: Probabilities do not sum to 1.")
    else:
        print("SUCCESS: Probabilities valid.")

    # 3. Save/Load
    model.save("test_model")
    loaded = HMMModel.load("test_model")
    print("Model saved and loaded successfully.")

if __name__ == "__main__":
    verify_hmm()
