import logging
import azure.functions as func
import json
import joblib
import os

# Load model (do this outside function so it loads once)
model_path = os.path.join(os.path.dirname(__file__), '../decision_tree_model.joblib')
model = joblib.load(model_path)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('🚪 Gateway function triggered.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    try:
        # Extract features
        features = [
            req_body.get('sensor_temp', 0),
            req_body.get('sensor_gas', 0),
            req_body.get('sensor_co', 0),
            req_body.get('sensor_sound', 0),
            req_body.get('sensor_smoke', 0)
        ]

        # Predict
        prediction = model.predict([features])[0]
        req_body['anomaly_flag'] = bool(prediction)

        return func.HttpResponse(
            json.dumps({"status": "Processed with ML", "processed_data": req_body}),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error processing ML: {e}")
        return func.HttpResponse("Error processing ML", status_code=500)
