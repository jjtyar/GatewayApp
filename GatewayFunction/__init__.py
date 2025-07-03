import logging
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('🚪 Gateway function triggered.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    # Example: Basic ML processing - simple rule for now
    sound_level = req_body.get('sensor_sound', 0)
    if sound_level > 70:
        req_body['anomaly_flag'] = True
    else:
        req_body['anomaly_flag'] = False

    # TODO: Connect to Azure IoT Hub here and forward data

    return func.HttpResponse(
        json.dumps({"status": "Processed", "processed_data": req_body}),
        mimetype="application/json",
        status_code=200
    )
