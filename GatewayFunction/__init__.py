import logging
import azure.functions as azuref
import json

def main(req: azuref.HttpRequest) -> azuref.HttpResponse:
    logging.info('🚪 Gateway function triggered.')

    return azuref.HttpResponse(
        json.dumps({"status": "Function is f reachable"}),
        mimetype="application/json",
        status_code=200
    )
