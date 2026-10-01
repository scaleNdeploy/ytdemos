class DeadServer(Exception):
    pass


class _FakeConn:
    def run(self, cmd):
        pass


def ssh_connect(host):
    if host == "srv-2":
        raise DeadServer(
            f"no route to {host}")
    return _FakeConn()


def deploy_to_servers(
        servers, connect=ssh_connect):
    failures = []
    for host in servers:
        try:
            conn = connect(host)
            conn.run("sync_code.sh")
        except Exception as e:
            print(f"warning: {host} "
                  f"did not update: {e}")
            failures.append(host)
    return len(failures) == 0


if __name__ == "__main__":
    ok = deploy_to_servers(
        ["srv-1", "srv-2", "srv-3"])
    print("deploy successful:", ok)
