import logging
import azure.functions as func
import json
import joblib
import os
from azure.iot.device import IoTHubDeviceClient, Message




# Load model
model_path = os.path.join(os.path.dirname(__file__), '../decision_tree_model.joblib')
model = joblib.load(model_path)
logging.info(f'Model path: {os.path.abspath(model_path)}')

# IoT Hub Device Connection String
IOTHUB_DEVICE_CONNECTION_STRING = "HostName=homesafetyhub.azure-devices.net;DeviceId=gatewaydevice;SharedAccessKey=8HLMsfUW4hRaJuoIq3HvNTj4USn2rqvof8jF9qaLkBs="

# Create IoT Hub client
device_client = IoTHubDeviceClient.create_from_connection_string(IOTHUB_DEVICE_CONNECTION_STRING)

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

        return func.HttpResponse(
            json.dumps({"status": "Processed and sent to IoT Hub", "processed_data": req_body}),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse("Error processing request.", status_code=500)
