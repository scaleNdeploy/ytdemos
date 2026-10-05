import notify
from logsetup import setup

FAKE = "TEST_TOKEN_123"

def test_token_not_in_logs(monkeypatch, capsys):
    monkeypatch.setenv("CARRIER_TOKEN", FAKE)
    setup()
    notify.notify("A-1042")
    logs = capsys.readouterr().err
    assert FAKE not in logs, "token leaked into logs"
