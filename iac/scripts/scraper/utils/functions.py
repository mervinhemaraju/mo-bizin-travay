import json
import logging
from kink import di
from models.db.opening_dao import ItemDao


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
        json_file.write(json.dumps([vars(opening) for opening in openings]))


def db_transact(openings: list):
    # Create a new ItemDao object
    item_dao = ItemDao()

    # Log event
    logging.info("Retrieving previous openings...")

    # Retrieve the previous openings
    previous_openings = item_dao.get_items_by_source(source=di["SOURCE"])

    # Log event
    logging.info(
        f"{len(previous_openings)} previous openings obtained from recruiter {di['SOURCE']}"
    )

    # Clear the previous openings from that recruiter
    item_dao.delete_all(openings=previous_openings)

    # Log event
    logging.info("Previous openings deleted")

    # Save the new openings
    item_dao.save_all(openings=openings)

    # Log event
    logging.info("New openings saved successfully")
