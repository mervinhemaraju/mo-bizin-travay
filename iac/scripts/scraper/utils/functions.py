import json
import logging
from kink import di
from models.db.dao import Dao


def post_to_slack(blocks, thread_ts=None, channel=None, text=None):
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


def db_transact(openings: list):
    # Create a new Dao object
    dao = Dao()

    # Clear the previous openings from that recruiter
    count = dao.delete_by_source(opening_source=di["SOURCE"])

    # Log event
    logging.info(f"{count} previous openings deleted from source {di['SOURCE']}")

    # Save the new openings
    dao.insert_all(documents=openings)

    # Log event
    logging.info("New openings saved successfully")
