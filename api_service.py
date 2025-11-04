import joblib

MODEL_FILE = 'models/fraud_model.joblib'
model_pipeline = None
try:
    model_pipeline = joblib.load(MODEL_FILE)
except FileNotFoundError:
    print(f"FATAL ERROR: Model file '{MODEL_FILE}' not found.")
    exit()
except Exception as e:
    print(f"Error loading model: {e}")
    exit()