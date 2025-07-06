import logging
import azure.functions as func

def main(event: func.EventHubEvent):
    for e in event:
        message = e.get_body().decode('utf-8')
        logging.info(f"📥 New IoT Hub message: {message}")
        # TODO: Optionally save to Blob or broadcast to Control Room
