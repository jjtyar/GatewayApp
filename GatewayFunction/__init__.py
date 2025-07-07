import logging
import azure.functions as func
import json
import joblib
import os
from azure.iot.device import IoTHubDeviceClient, Message
from azure.storage.blob import BlobServiceClient

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'decision_tree_model.joblib')
model = joblib.load(model_path)

# IoT Hub Device Connection String (consider moving this to App Settings later)
IOTHUB_DEVICE_CONNECTION_STRING = "HostName=homesafetyhub.azure-devices.net;DeviceId=gatewaydevice;SharedAccessKey=8HLMsfUW4hRaJuoIq3HvNTj4USn2rqvof8jF9qaLkBs="
device_client = IoTHubDeviceClient.create_from_connection_string(IOTHUB_DEVICE_CONNECTION_STRING)

# Azure Blob Storage Setup
BLOB_CONNECTION_STRING = os.getenv('BLOB_CONNECTION_STRING')  # ✅ Securely loaded from App Settings
BLOB_CONTAINER_NAME = "sensordata"
BLOB_FILE_NAME = "sensor_data.json"

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

        # Update Blob Storage
        update_blob(req_body)

        return func.HttpResponse(
            json.dumps({"status": "Processed, sent to IoT Hub, and updated Blob", "processed_data": req_body}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse("Error processing request.", status_code=500)

def update_blob(new_event):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
        blob_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME).get_blob_client(BLOB_FILE_NAME)

        try:
            # Try to download existing data
            blob_data = blob_client.download_blob().readall()
            sensor_data = json.loads(blob_data)
        except Exception:
            # If blob does not exist or is empty
            sensor_data = []

        sensor_data.append(new_event)

        # Upload updated data (overwrite existing blob)
        blob_client.upload_blob(json.dumps(sensor_data), overwrite=True)

        logging.info('✅ Blob updated f successfully.')

    except Exception as e:
        logging.error(f"Error updating blob: {e}")
