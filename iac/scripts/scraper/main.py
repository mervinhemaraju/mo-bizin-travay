import logging
import importlib.util
from kink import di
from models.core.di import main_injection
from models.core.exceptions import DryRunException
from utils.functions import post_to_slack, file_transact, db_transact
from utils.slack_blocks import block_completed, block_error, block_info

# Initialize Logging
logging.getLogger().setLevel(logging.INFO)


@main_injection
def main(event, context):
    # Define empty openings list
    openings = []

    # Post message to slack
    _, thread_ts = post_to_slack(
        blocks=block_info(
            message=f"Trigerred from source `{di['SOURCE']}` with url `{di['SOURCE_URL']}`"
        )
    )

    try:
        # Get the dry run flag
        dry_run = "dry_run" in event

        # Log event if it is a dry run
        if dry_run:
            logging.info("Event running in dry run mode.")

        # Retrieve event parameters
        delay = event["delay"] if "delay" in event else di["DELAY"]

        # Load the module
        spec = importlib.util.spec_from_file_location(
            di["SOURCE"], f"entities/{di['SOURCE']}.py"
        )
        entity = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(entity)

        # ! scrape the data
        openings = entity.scrape(delay=delay, dry_run=dry_run)

        if len(openings) > 0:
            # Log event
            logging.info(
                f"{len(openings)} openings obtained from source {di['SOURCE']}"
            )

            # Post to slack
            post_to_slack(
                blocks=block_info(
                    message=f"`{len(openings)}` openings obtained from source `{di['SOURCE']}`"
                ),
                thread_ts=thread_ts,
            )

        # Verify if this is a dry run
        if dry_run:
            # Log event
            logging.info("Dry run detected. No data will be saved.")

            # Post to slack
            post_to_slack(
                blocks=block_info(message="Script is running in `dry run` mode"),
                thread_ts=thread_ts,
            )

            # Log event
            # logging.info(
            #     f"{len(openings)} The following titles were obtained: {[o for o in openings]}"
            # )

            # Export openings to json file
            file_transact(openings=openings)

            # ! Raise exception
            raise Exception("Dry run completed. No data was saved.")

        # Save openings to DB
        db_transact(openings)

        # Log event
        logging.info("Script completed successfully.")

        # Post to slack
        post_to_slack(blocks=block_completed(), thread_ts=thread_ts)

    except DryRunException as dre:
        # Log error
        logging.error(f"Dry Run initiated: {dre}")

        # Post to slack
        post_to_slack(
            blocks=block_error(error_message="Dry run completed."),
            thread_ts=thread_ts,
        )

    except Exception as e:
        # Log error
        logging.error(f"Error occurred: {str(e)}")

        # Post to slack
        post_to_slack(blocks=block_error(error_message=str(e)), thread_ts=thread_ts)
