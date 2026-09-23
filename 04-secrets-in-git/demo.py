"""Runs the whole story from the video, end to end, in a throwaway
git repo (created under a temp directory, never inside this repo).

Requires: git, and gitleaks on your PATH (https://github.com/gitleaks/gitleaks).
Run:
    python demo.py
"""
import os
import shutil
import subprocess
import tempfile

from generate_secrets import (
    settings_with_secrets,
    fake_ssh_private_key,
    SETTINGS_ENV,
)

PRE_COMMIT = open(os.path.join(os.path.dirname(__file__), "pre-commit")).read()


def sh(cmd, cwd, env=None):
    print(f"$ {cmd}")
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, env=env)
    out = (p.stdout + p.stderr).strip()
    if out:
        print(out)
    print()
    return p


def section(title):
    print("\n=== " + title + " ===")


def main():
    repo = tempfile.mkdtemp(prefix="secrets-demo-")
    print(f"Working in a throwaway repo: {repo}\n")
    env = dict(os.environ, GIT_AUTHOR_NAME="dev", GIT_AUTHOR_EMAIL="dev@payments.test",
               GIT_COMMITTER_NAME="dev", GIT_COMMITTER_EMAIL="dev@payments.test")
    subprocess.run("git init -q -b main", shell=True, cwd=repo, env=env)

    section("1. The mistake: commit real-looking secrets")
    open(os.path.join(repo, "settings.py"), "w").write(settings_with_secrets())
    open(os.path.join(repo, "deploy_key"), "w").write(fake_ssh_private_key())
    subprocess.run('git add . && git commit -q -m "add settings"', shell=True, cwd=repo, env=env)
    print("Committed. Looks fine, nobody looks twice.\n")

    section("2. Scan the history with gitleaks")
    sh("gitleaks git . -v", repo, env=env)

    section("3. The wrong fix: take secrets out of the current file")
    open(os.path.join(repo, "settings.py"), "w").write(SETTINGS_ENV)
    open(os.path.join(repo, "deploy_key"), "w").write("")
    subprocess.run('git commit -aqm "remove keys"', shell=True, cwd=repo, env=env)
    print("Scan the working files (clean):")
    sh("gitleaks dir .", repo, env=env)
    print("Scan the full history (still finds them):")
    sh("gitleaks git .", repo, env=env)
    print("Deleting a line does not delete history.\n")

    section("4. Prevention: block it before it is ever committed")
    shutil.copy(os.path.join(os.path.dirname(__file__), "pre-commit"),
                os.path.join(repo, ".git", "hooks", "pre-commit"))
    os.chmod(os.path.join(repo, ".git", "hooks", "pre-commit"), 0o755)
    with open(os.path.join(repo, "settings.py"), "a") as f:
        f.write(f'TEST_KEY = "{settings_with_secrets().splitlines()[1].split(" = ")[1]}"\n')
    r = sh('git commit -am test', repo, env=env)
    sh("git log --oneline", repo, env=env)
    if r.returncode != 0:
        print("Blocked. The commit never happened. The key never reached history.")
    else:
        print("(Hook did not block this run — check that gitleaks is installed and on PATH.)")

    print(f"\nCleaning up {repo}")
    shutil.rmtree(repo, ignore_errors=True)


if __name__ == "__main__":
    main()
