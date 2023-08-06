# Send Email Notification

[![Build Image](https://github.com/licenseware/send-email-notification/actions/workflows/build-image.yml/badge.svg)](https://github.com/licenseware/send-email-notification/actions/workflows/build-image.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Using [the Python library](https://pypi.org/project/sendgrid/), send email to people
with the content & subject of your choice.

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

## Send email to multiple address upon Github release

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
