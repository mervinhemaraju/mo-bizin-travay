from kink import di


def post_to_slack(blocks, thread_ts=None, channel=None):
    response = di["slack_wc"].chat_postMessage(
        channel=di["SLACK_CHANNEL_MAIN"] if channel is None else channel,
        text=None,
        attachments=blocks,
        thread_ts=thread_ts,
    )
    return response, response["ts"]
