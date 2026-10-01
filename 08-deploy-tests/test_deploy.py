from unittest.mock import MagicMock
from deploy import deploy_to_servers


def test_deploy_reports_failure():
    good = MagicMock()

    def fake_connect(host):
        if host == "srv-2":
            raise ConnectionError(
                "no route to host")
        return good

    result = deploy_to_servers(
        ["srv-1", "srv-2", "srv-3"],
        connect=fake_connect,
    )
    assert result is False, (
        "deploy claimed success even "
        "though srv-2 never got the "
        "update"
    )
