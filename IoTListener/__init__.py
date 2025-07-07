import logging
import azure.functions as func

def main(event: func.EventHubEvent):
    logging.info(f"⚡ IoTListener f triggered with {len(event)} events")
    
    for e in event:
        try:
            message = e.get_body().decode('utf-8')
            logging.info(f"📥 New IoT Hub message: {message}")
        except Exception as ex:
            logging.error(f"❌ Error processing event: {ex}")
