# A bucket policy that's too open

Video: not uploaded yet
Short: not uploaded yet

Needs Python 3.10 or newer, plus:

    pip install boto3 moto

No real AWS account or credentials are used or required. Every AWS call
here runs against `moto`, a library that mocks AWS in-process.

## Run it

The mistake only, showing who ends up with read access:

    python main_before.py

The full run: the mistake, then the fix:

    python main.py

Expected output from `main.py`:

    Before the fix:
      http://acs.amazonaws.com/groups/global/AuthenticatedUsers -> READ
    After the fix:
      northridge-owner -> FULL_CONTROL
    Block public access: True

## What this shows

A fictional company ("northridge") puts a customer report in an S3
bucket, then grants read access to the "Authenticated Users" group,
intending to mean "our own team". AWS defines that group as any AWS
account holder, not a specific team; anyone can sign up for a free AWS
account. The fix: turn on S3 Block Public Access, and grant reads to a
specific owner by name instead of a group.

Since April 2023, AWS turns on S3 Block Public Access by default for
every new bucket, so this exact mistake is harder to make by accident
today than it was when the real-world incident below happened.

## Real-world source

This mistake mirrors a real, public incident: in 2017, a Dow Jones S3
bucket was set to "Authenticated Users" and exposed data on millions of
real customers, discovered and documented by UpGuard:
https://www.upguard.com/breaches/cloud-leak-dow-jones

## Limits

No real AWS account, bucket, or data is involved anywhere in this repo.
`moto` mimics the AWS APIs used here (S3 bucket, object, ACL, and
public-access-block calls); it does not model every AWS behavior or
edge case.
