# Your logs are leaking tokens

Video: https://youtu.be/4IZiquSegz4
Short: https://youtube.com/shorts/2VfA4cZJNTQ

Needs Python 3.10 or newer and pytest (tested with Python 3.10.12, pytest 9.1.1).

    pip install -r requirements.txt

Everything here is fictional: the company (parcelpath), its notify service,
the carrier and both tokens. `pp_live_9f3kX2qW` and `TEST_TOKEN_123` are
fake. Never put a real token in an example like this.

## The three steps

Each folder is the code at one point in the video. Set a fake token first.

    # macOS / Linux
    export CARRIER_TOKEN=pp_live_9f3kX2qW
    # Windows (PowerShell)
    $env:CARRIER_TOKEN = "pp_live_9f3kX2qW"

**step1 - the leak.** A late-night debug line logs the request headers,
token included.

    cd step1
    python notify.py      # the full token shows up in the log
    pytest -q             # FAILS: the fake test token reached the logs

**step2 - the fix.** `logsetup.py` gets a formatter that scrubs anything that
looks like a secret (`Bearer ...`, `token=...`, `password=...`) from the
final text of every log line. `notify.py` and the test are unchanged.

    cd step2
    python notify.py      # Bearer ****
    pytest -q             # passes

**step3 - the crash.** A tracking call puts the token in the web address,
and a timeout puts that address in the traceback. Because the scrub runs on
the final text, the traceback is cleaned too. A second test covers it.

    cd step3
    python notify.py      # ...track?token=****
    pytest -q             # 2 passed

## How the test works

`test_logs.py` sets a fake token, runs the code, and reads what the app
really wrote to stderr (`capsys`), not a copy made only for the test. If the
fake token appears, the test fails. Run it in CI on every push.

Why a test and not only a scanner: secret scanners look for keys written in
your files. `step1/notify.py` has no key in it. The token only appears when
the code runs.

## Limits

- The scrub only catches the patterns you give it. That's why the test stays.
- A test only covers the code paths it runs. Add one for each path that logs
  request data or errors.
- If a token has already leaked, deleting the logs is not enough. Rotate it:
  cancel the old token and issue a new one.

## Real-world anchor

- Twitter, 3 May 2018: "passwords were written to an internal log before
  completing the hashing process." Twitter found it, removed the passwords,
  and asked users to consider changing their passwords.
  https://blog.x.com/official/en_us/topics/company/2018/keeping-your-account-secure.html
- Irish Data Protection Commission, 27 Sep 2024: Meta fined EUR 91 million
  over passwords stored in plain text on its internal systems.
  https://www.dataprotection.ie/en/news-media/press-releases/DPC-announces-91-million-fine-of-Meta

Those two are real. The rest of this folder is a fictional company built to
show the same mistake on a small scale.
