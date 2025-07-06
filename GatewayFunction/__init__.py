import logging
import azure.functions as func
import json
import joblib
import os
from azure.iot.device import IoTHubDeviceClient, Message
from azure.storage.blob import BlobClient

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'decision_tree_model.joblib')
model = joblib.load(model_path)
logging.info(f'Model path: {os.path.abspath(model_path)}')

# IoT Hub Device Connection String
IOTHUB_DEVICE_CONNECTION_STRING = "HostName=homesafetyhub.azure-devices.net;DeviceId=gatewaydevice;SharedAccessKey=8HLMsfUW4hRaJuoIq3HvNTj4USn2rqvof8jF9qaLkBs="
device_client = IoTHubDeviceClient.create_from_connection_string(IOTHUB_DEVICE_CONNECTION_STRING)

# Azure Blob Storage
BLOB_URL = "https://publicanonymousaccount.blob.core.windows.net/sensordata/sensor_data.json"
SAS_TOKEN = "sp=rw&st=2025-07-06T10:38:07Z&se=2025-12-12T18:38:07Z&spr=https&sv=2024-11-04&sr=c&sig=qLnGUgDUGsJHzzf7%2FvRABNkTCexK8870iRUdgGfzGvg%3D"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('🚪 Gateway function triggered.')

    try:
        req_body = req.get_json()

        # Extract features for ML
        features = [
            req_body.get('sensor_temp', 0),
            req_body.get('sensor_gas', 0),
            req_body.get('sensor_co', 0),
            req_body.get('sensor_sound', 0),
            req_body.get('sensor_smoke', 0)
        ]

        # Predict anomaly
        prediction = model.predict([features])[0]
        req_body['anomaly_flag'] = bool(prediction)

        # Send message to Azure IoT Hub
        iot_message = Message(json.dumps(req_body))
        device_client.send_message(iot_message)
        logging.info('✅ Message sent to IoT Hub.')

        # Update Azure Blob Storage
        update_blob(req_body)

        return func.HttpResponse(
            json.dumps({"status": "Processed, sent to IoT Hub, and saved to Blob", "processed_data": req_body}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse("Error processing request.", status_code=500)

def update_blob(new_event):
    try:
        blob_client = BlobClient.from_blob_url(f"{BLOB_URL}?{SAS_TOKEN}")
        try:
            # Try to download existing data
            existing_data = json.loads(blob_client.download_blob().readall())
        except Exception:
            # If blob is empty or missing, start with an empty list
            logging.warning("Blob not found or empty. Starting a new file.")
            existing_data = []

        # Append the new event
        existing_data.append(new_event)

        # Upload the updated list
        blob_client.upload_blob(json.dumps(existing_data), overwrite=True)
        logging.info('✅ Blob updated successfully.')

    except Exception as e:
        logging.error(f"❌ Error updating blob: {e}")
