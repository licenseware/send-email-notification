# Send Email Notification

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](./.pre-commit-config.yaml)
[![License](https://img.shields.io/github/license/licenseware/send-email-notification)](./LICENSE)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Send Email Notification](#send-email-notification)
  - [Send email to one address](#send-email-to-one-address)
  - [Send email to multiple addresses upon Github release](#send-email-to-multiple-addresses-upon-github-release)
  - [Send email with attachments](#send-email-with-attachments)
  - [Run Docker Container Locally](#run-docker-container-locally)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Using [the Sendgrid Python library](https://pypi.org/project/sendgrid/), send
email to people with the content & subject of your choice.

This repository is used inside Github Actions in the following format:

## Send email to one address

```yaml
      - uses: licenseware/send-email-notification@v1
        with:
          api-key: ${{ secrets.SENDGRID_API_KEY }}
          subject: Test Subject
          from-email: verified-email@licenseware.io
          to-email: john-doe@licenseware.io
          markdown-body: |
            # My Markdown Title

            This is a description

            ## Another header

            Another description
```

## Send email to multiple addresses upon Github release

```yaml
on:
  release:
    types:
      - published

jobs:
  release-notification:
    name: release notification
    runs-on: ubuntu-latest
    strategy:
      matrix:
        to-emails:
          - receiver1@licenseware.io
          - receiver2@licenseware.io
          - receiver3@licenseware.io

    steps:
      - uses: licenseware/send-email-notification@v1
        with:
          api-key: ${{ secrets.SENDGRID_API_KEY }}
          subject: New Release ${{ github.repository }}:${{ github.ref_name }}
          from-email: verified-email@licenseware.io
          to-email: ${{ matrix.to-emails }}
          markdown-body: ${{ github.event.release.body }}

```

## Send email with attachments

```yaml
      - uses: licenseware/send-email-notification@v1
        with:
          api-key: ${{ secrets.SENDGRID_API_KEY }}
          subject: Test Subject
          from-email: verified-email@licenseware.io
          to-email: some-dude@licenseware.io
          markdown-body: |
            Hey, check out this file
          attachments: |
            ./path/to/file1.txt
            ./path/to/file2.txt
          # optionally, a list of zero, one, or the same size {inline, attachment}
          attachments-disposition: |
            attachment
            attachment
```

## Run Docker Container Locally

Grab the latest tag from here:

[![GitHub Tag](https://img.shields.io/github/v/tag/licenseware/send-email-notification?sort=semver&style=plastic&label=latest%20tag&color=light-green)](https://github.com/licenseware/send-email-notification/pkgs/container/send-email-notification)

```bash
export SENDGRID_API_KEY="CHANGE_THIS"

docker run --rm \
  --name send-email-notification \
  ghcr.io/licenseware/send-email-notification \
  --api-key=${SENDGRID_API_KEY} \
  --from=info@example.com \
  --to=john@example.com \
  --subject="Send email notifications" \
  --markdown-body="""
# Send email notifications

Checkout this cool repository:

<https://github.com/licenseware/send-email-notification>
"""
```
