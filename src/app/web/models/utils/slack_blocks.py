VALUE_COLOR_STATEMENT = "#ffac5a"


def block_message(sender_name, sender_subject, sender_email, message):
    return [
        {
            "color": VALUE_COLOR_STATEMENT,
            "blocks": [
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"A message was sent by `{sender_name}` from Mo Bizin Travay",
                        }
                    ],
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"Email: {sender_email}",
                        }
                    ],
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"Subject: *{sender_subject}*",
                        }
                    ],
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"```{message}```",
                        }
                    ],
                },
            ],
        }
    ]
