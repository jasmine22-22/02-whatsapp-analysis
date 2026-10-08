import re
from pathlib import Path

import pandas as pd

_DATETIME_FORMAT = "%m/%d/%y, %I:%M %p"
_MESSAGE_START = re.compile(
    r"^(?P<datetime>\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m)\s-\s(?P<content>.*)$",
    re.IGNORECASE,
)
_SYSTEM_SENDERS = {"system", "whatsapp"}


def parse_chat(path):
    """Parse a WhatsApp text export into datetime, sender, and message columns."""
    messages = []
    current_message = None

    with Path(path).open("r", encoding="utf-8") as chat_file:
        for raw_line in chat_file:
            line = raw_line.rstrip("\r\n")
            match = _MESSAGE_START.match(line)

            if match:
                if current_message is not None:
                    messages.append(current_message)

                sender, separator, message = match.group("content").partition(": ")
                if not separator or sender.casefold() in _SYSTEM_SENDERS:
                    current_message = None
                    continue

                current_message = {
                    "datetime": match.group("datetime"),
                    "sender": sender,
                    "message": message,
                }
            elif current_message is not None:
                current_message["message"] += "\n" + line

    if current_message is not None:
        messages.append(current_message)

    frame = pd.DataFrame(messages, columns=["datetime", "sender", "message"])
    frame["datetime"] = pd.to_datetime(
        frame["datetime"], format=_DATETIME_FORMAT
    )
    return frame
