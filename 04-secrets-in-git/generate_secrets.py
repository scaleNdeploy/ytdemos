"""Generates fresh, random, fake secrets for the demo below.

Nothing here is a real credential, and nothing here is committed to this
repo: every value is random each time you run it, so there is nothing
static for a secret scanner to find in this repository's own history.
"""
import random
import string


def _rand(n, alphabet=string.ascii_uppercase + string.digits):
    return "".join(random.choices(alphabet, k=n))


def fake_aws_key_id():
    # Shape of a real AWS access key ID (AKIA + 16 chars), so a scanner
    # like gitleaks recognizes it the same way it would a real one.
    return "AKIA" + _rand(16)


def fake_aws_secret():
    alphabet = string.ascii_letters + string.digits + "+/"
    return _rand(40, alphabet)


def fake_db_password():
    return _rand(14, string.ascii_letters + string.digits)


def fake_ssh_private_key():
    # Built from parts, not a literal header string, so this file has
    # nothing static for a secret scanner to flag (the demo still
    # produces a real-looking header at runtime).
    tag = "PRIVATE" + " " + "KEY"
    begin = "-" * 5 + "BEGIN OPENSSH " + tag + "-" * 5
    end = "-" * 5 + "END OPENSSH " + tag + "-" * 5
    alphabet = string.ascii_letters + string.digits + "+/"
    lines = [_rand(49, alphabet) for _ in range(3)]
    return begin + "\n" + "\n".join(lines) + "\n" + end + "\n"


def settings_with_secrets():
    return (
        "# payments-api settings (fake values, generated fresh)\n"
        f'AWS_KEY = "{fake_aws_key_id()}"\n'
        f'AWS_SECRET = "{fake_aws_secret()}"\n'
        f'DB_PASSWORD = "{fake_db_password()}"\n'
    )


SETTINGS_ENV = '''import os

# payments-api settings
AWS_KEY = os.environ["AWS_KEY"]
AWS_SECRET = os.environ["AWS_SECRET"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
'''
