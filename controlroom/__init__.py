import azure.functions as func
from azure.storage.blob import BlobServiceClient
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Azure Blob Storage connection details
    blob_connection_string = "DefaultEndpointsProtocol=https;AccountName=publicanonymousaccount;AccountKey=WvptbsFWaE7uE6jlRohJSEcWEDSGqWDEVc1yX4vYS9Fte27k70Lh9GbuP0k/B/d/weENMqiLYi2t+AStYhMs8A==;EndpointSuffix=core.windows.net"
    container_name = "sensordata"
    blob_name = "sensor_data.json"

    try:
        # Connect to the blob
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        blob_client = blob_service_client.get_container_client(container_name).get_blob_client(blob_name)

        # Read the blob content
        blob_data = blob_client.download_blob().readall()
        data = json.loads(blob_data)

        # Return the JSON data as HTTP response
        return func.HttpResponse(
            json.dumps(data),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )
