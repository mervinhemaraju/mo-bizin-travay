import json
import logging
from kink import di
from models.services.mongoapi import MongoAPI


def post_to_slack(blocks, thread_ts=None, channel=None, text="`mo-bizin-travay`"):
    # * Posts the message to slack
    response = di["slack_wc"].chat_postMessage(
        channel=di["SLACK_CHANNEL"] if channel is None else channel,
        text=text,
        attachments=blocks,
        thread_ts=thread_ts,
    )

    # * Returns the full response and the thread ts code
    return response, response["ts"]


def file_transact(openings: list):
    with open(f"mo-bizin-travay-{di['SOURCE'].lower()}.json", "w") as json_file:
        json_file.write(json.dumps([opening for opening in openings]))


def db_transact(openings: list[dict]):
    # Create a new API object
    api = MongoAPI()

    # Clear the previous openings from that recruiter
    count = api.delete_by_source(opening_source=di["SOURCE"])

    # Log event
    logging.info(f"{count} previous openings deleted from source {di['SOURCE']}")

    # Save the new openings
    save_response = api.save_all(documents=openings)

    # Verify if save is a success
    if save_response["success"]:
        # Log event
        logging.info(f"{save_response['count']} new openings saved successfully.")
    else:
        #! Raise an exception is save unsuccessfull
        raise Exception(f"Error while saving new openings: {save_response['message']}")
