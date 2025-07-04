import logging
import azure.functions as azuref
import json

def main(req: azuref.HttpRequest) -> azuref.HttpResponse:
    logging.info('🚪 Gateway function triggered.')

    req_body = req.get_json()
        features = [
            req_body.get('sensor_temp', 0),
            req_body.get('sensor_gas', 0)
        ]    

        logging.info('sensor_temp is=')
        logging.info(req_body.get('sensor_temp', 0))


    return azuref.HttpResponse(
        json.dumps({"status": "Function is f reachable"}),
        mimetype="application/json",
        status_code=200
    )

