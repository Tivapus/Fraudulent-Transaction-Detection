import joblib
import pandas as pd
import uvicorn
from fastapi import FastAPI
from api_models import Transaction
from database import database, fraudulent_transactions
from contextlib import asynccontextmanager
from model_feature_engineer import AccountFeatureEngineer


# Model Loading
MODEL_FILE = 'model/fraud_model.joblib'
model_pipeline = None
try:
    model_pipeline = joblib.load(MODEL_FILE)
except FileNotFoundError:
    print(f"FATAL ERROR: Model file '{MODEL_FILE}' not found.")
    exit()
except Exception as e:
    print(f"Error loading model: {e}")
    exit()


# Api
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield

    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
async def predict_fraud(transaction: Transaction):
    """
    Endpoint 1: ทำนายธุรกรรม (POST)
    รับ JSON ธุรกรรม และคืนผลลัพธ์
    """
    try:
        data_dict = transaction.model_dump()
       
        input_df = pd.DataFrame([data_dict])

        prediction = model_pipeline.predict(input_df)
        result = int(prediction[0])

        if result == 1:
            query = fraudulent_transactions.insert().values(**data_dict)
            await database.execute(query)

        return {"is_fraud": result}

    except Exception as e:
        print(f"Error during prediction: {e}")
        return {"error": str(e)}, 500

@app.get("/frauds")
async def get_all_frauds():
    """
    Endpoint 2: ดึงข้อมูลการโกงทั้งหมด (GET)
    คืนค่า JSON list ของทุกธุรกรรมที่เคยถูกบันทึกว่าโกง
    """
    try:
        query = fraudulent_transactions.select().order_by(fraudulent_transactions.c.time_ind.desc())
       
        results = await database.fetch_all(query)
       
        return results

    except Exception as e:
        print(f"Error fetching from DB: {e}")
        return {"error": str(e)}, 500

@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is running. Go to /docs for Swagger UI."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)