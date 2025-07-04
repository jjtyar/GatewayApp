import logging
import azure.functions as azuref
import json

def main(req: azuref.HttpRequest) -> azuref.HttpResponse:
    logging.info('🚪 Gateway function fef triggered.')

    try:
        req_body = req.get_json()

        features = [
            req_body.get('sensor_temp', 0),
            req_body.get('sensor_gas', 0)
        ]    

        logging.info('sensor_temp is = {}'.format(req_body.get('sensor_temp', 0)))

        return azuref.HttpResponse(
            json.dumps({"status": "Function is reachable", 'sensor_temp is = {}'.format(req_body.get('sensor_temp', 0)) }),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error: {e}")
        return azuref.HttpResponse("Error in processing request", status_code=500)
