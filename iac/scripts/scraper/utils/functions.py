from kink import di


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
