import logging
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('🚪 Gateway function triggered.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    sound_level = req_body.get('sensor_sound', 0)
    req_body['anomaly_flag'] = sound_level > 70

    logging.info(f"Processed Data: {req_body}")

    return func.HttpResponse(
        json.dumps({"status": "Processed", "processed_data": req_body}),
        mimetype="application/json",
        status_code=200
    )
