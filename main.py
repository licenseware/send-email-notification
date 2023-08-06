#!/usr/bin/env python

import argparse
import base64
import enum
import pathlib
import sys

import magic
import markdown
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    ContentId,
    Disposition,
    FileContent,
    FileName,
    FileType,
    Mail,
)


class AttachmentDisposition(str, enum.Enum):
    INLINE = "inline"
    ATTACHMENT = "attachment"
    EMPTY = ""  # no disposition provided by the user (default CLI behavior)

    def __str__(self):
        return self.value


parser = argparse.ArgumentParser()
parser.add_argument(
    "--to",
    dest="to_email",
    type=str,
    nargs="+",
    action="extend",
    required=True,
    help="Email address to send the notification to",
)
parser.add_argument("--subject", type=str, required=True, help="Subject of the email")
parser.add_argument(
    "--markdown-body", type=str, required=True, help="Body of the email"
)
parser.add_argument(
    "--from",
    dest="from_email",
    type=str,
    required=True,
    help="Email address to send the notification from",
)
parser.add_argument("--api-key", type=str, required=True, help="SendGrid API key")
parser.add_argument(
    "--attachments",
    type=str,
    nargs="*",
    help="Space separated file paths to attach to the email",
)
parser.add_argument(
    "--attachments-disposition",
    type=str,
    nargs="*",
    help="Attachment disposition (default: attachment). Specify only one to apply to all attachments, or none at all to use the default.",
    choices=list(AttachmentDisposition),
    # the default is not approved by the author of this code, but we don't want
    # to confuse the user by having different defaults than that of the SendGrid.
    default=[AttachmentDisposition.ATTACHMENT],
)


def add_attachments(message: Mail, attachments: list, dispositions: list):
    if len(dispositions) == 1 and dispositions[0] == AttachmentDisposition.EMPTY:
        dispositions = []

    if not dispositions:
        dispositions = [AttachmentDisposition.ATTACHMENT] * len(attachments)
    elif len(dispositions) == 1:
        dispositions = [dispositions[0]] * len(attachments)
    elif len(attachments) != len(dispositions):
        raise ValueError("Number of attachments and dispositions must be the same")
    for filepath, disposition in zip(attachments, dispositions):
        filepath = filepath.strip("\n")
        with open(filepath, "rb") as f:
            file_content = f.read()
        encoded_file = base64.b64encode(file_content).decode()
        mimetype = magic.from_file(filepath, mime=True)
        filename = pathlib.Path(filepath).name
        attachment = Attachment(
            FileContent(encoded_file),
            FileName(filename),
            FileType(mimetype),
            Disposition(disposition),
            ContentId(filename),
        )
        message.add_attachment(attachment)


def is_attachment_requested(attachments: list):
    return bool(attachments) and attachments != [""]


if __name__ == "__main__":
    args = parser.parse_args()
    print(args)

    message = Mail(
        from_email=args.from_email,
        to_emails=args.to_email,
        subject=args.subject,
        html_content=markdown.markdown(args.markdown_body),
    )

    if is_attachment_requested(args.attachments):
        add_attachments(message, args.attachments, args.attachments_disposition)

    try:
        sg = SendGridAPIClient(args.api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as exp:
        sys.stderr.write(f"{exp}\n")
        exit(1)
