import logging
import azure.functions as azuref
import json

def main(req: azuref.HttpRequest) -> azuref.HttpResponse:
    logging.info('🚪 Gateway function flyeef triggered.')

    try:

        model_path = os.path.join(os.path.dirname(__file__), '../decision_tree_model.joblib')
model = joblib.load(model_path)
logging.info(f'Model path: {os.path.abspath(model_path)}')

        req_body = req.get_json()

        features = [
            req_body.get('sensor_temp', 0),
            req_body.get('sensor_gas', 0)
        ]    

        logging.info('sensor_temp is = {}'.format(req_body.get('sensor_temp', 0)))

        return azuref.HttpResponse(
            json.dumps({"sensor_temp": req_body.get('sensor_temp', 0)}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error: {e}")
        return azuref.HttpResponse("Error in processing request", status_code=500)
