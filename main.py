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
    "--attachments", type=str, nargs="*", help="File paths to attach to the email"
)
parser.add_argument(
    "--attachment-disposition",
    type=str,
    help="Attachment disposition (default: attachment)",
    choices=list(AttachmentDisposition),
    default=AttachmentDisposition.ATTACHMENT,
)


def add_attachments(message: Mail, attachments: list, disposition: str):
    for filepath in attachments:
        with open(filepath, "rb") as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()
        mimetype = magic.from_file(filepath, mime=True)
        filename = pathlib.Path(filepath).name
        message.attachment = Attachment(
            FileContent(encoded_file),
            FileName(filepath),
            FileType(mimetype),
            Disposition(disposition),
            ContentId(filename),
        )


if __name__ == "__main__":
    args = parser.parse_args()

    message = Mail(
        from_email=args.from_email,
        to_emails=args.to_email,
        subject=args.subject,
        html_content=markdown.markdown(args.markdown_body),
    )

    if args.attachments:
        add_attachments(message, args.attachments)

    try:
        sg = SendGridAPIClient(args.api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as exp:
        sys.stderr.write(f"{exp}\n")
        exit(1)
