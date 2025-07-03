import logging
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('🚪 Gateway function triggered.')

    return func.HttpResponse(
        json.dumps({"status": "F unction is reachable"}),
        mimetype="application/json",
        status_code=200
    )
