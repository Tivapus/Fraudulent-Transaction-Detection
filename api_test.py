import requests
import time

API_URL = "http://127.0.0.1:5000"

NORMAL_TRANSACTION_PAYLOAD = {
  "time_ind": 100,
  "transac_type": "PAYMENT",
  "amount": 1500.75,
  "src_acc": "C123456",
  "dst_acc": "M789012",
  "src_bal": 20000.0,
  "src_new_bal": 18499.25,
  "dst_bal": 0.0,
  "dst_new_bal": 0.0,
  "is_flagged_fraud": 0
}

FRAUD_TRANSACTION_PAYLOAD = {
  "time_ind": 100,
  "transac_type": "TRANSFER",
  "amount": 1500000000000.75,
  "src_acc": "C123456",
  "dst_acc": "M789012",
  "src_bal": 2000000000.0,
  "src_new_bal": 18499.25,
  "dst_bal": 5.0,
  "dst_new_bal": 0.0,
  "is_flagged_fraud": 1
}


def test_api_endpoints():
    """
    รันสคริปต์เพื่อทดสอบ API Endpoints
    """
    print(f"--- Starting API Test against {API_URL} ---")

    try:
        # --- TEST 1: POST /predict (Normal Transaction) ---
        print("\n[TEST 1] Sending NORMAL transaction to /predict ...")
        response_normal = requests.post(f"{API_URL}/predict", json=NORMAL_TRANSACTION_PAYLOAD)
        
        if response_normal.status_code == 200:
            result_normal = response_normal.json()
            print(f"✅ SUCCESS (200 OK): Got response: {result_normal}")
            assert result_normal == {"is_predicted_fraud": 0}
            print("✅ TEST 1 PASSED!")
        else:
            print(f"❌ FAILED (Status {response_normal.status_code}): {response_normal.text}")
            return

        # --- TEST 2: POST /predict (Fraud Transaction) ---
        print("\n[TEST 2] Sending FRAUD transaction to /predict ...")
        response_fraud = requests.post(f"{API_URL}/predict", json=FRAUD_TRANSACTION_PAYLOAD)
        
        if response_fraud.status_code == 200:
            result_fraud = response_fraud.json()
            print(f"✅ SUCCESS (200 OK): Got response: {result_fraud}")
            assert result_fraud == {"is_predicted_fraud": 1}
            print("... (API should be saving this to DB now) ...")
            print("✅ TEST 2 PASSED!")
        else:
            print(f"❌ FAILED (Status {response_fraud.status_code}): {response_fraud.text}")
            return

        # (รอ 1 วินาที เพื่อให้แน่ใจว่า API บันทึก DB เสร็จ)
        print("\n(Waiting 1 second for DB write...)")
        time.sleep(1)

        # --- TEST 3: GET /frauds (Check if saved) ---
        print("\n[TEST 3] Sending GET request to /frauds ...")
        response_get = requests.get(f"{API_URL}/frauds")
        
        if response_get.status_code == 200:
            fraud_list = response_get.json()
            print(f"✅ SUCCESS (200 OK): Found {len(fraud_list)} cases in DB.")
            
            found = False
            for case in fraud_list:
                if case.get("src_acc") == FRAUD_TRANSACTION_PAYLOAD.get("src_acc"):
                    found = True
                    break
            
            if found:
                print("✅ TEST 3 PASSED! (Found the saved fraud case in DB)")
            else:
                print("❌ FAILED: Did not find the new fraud case in the DB response.")
                
        else:
            print(f"❌ FAILED (Status {response_get.status_code}): {response_get.text}")
            return

        print("\n--- All Tests Completed Successfully! ---")

    except requests.exceptions.ConnectionError:
        print(f"\n❌ FATAL ERROR: Cannot connect to API at {API_URL}")
        print("💡 Make sure your API is running first!")
        print("   (Run 'python 3_api_service_fastapi.py' in another terminal)")

# --- Run the Test ---
if __name__ == "__main__":
    test_api_endpoints()