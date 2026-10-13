# An AI agent ran terraform destroy

Video: https://youtu.be/8Rr6IFJjAfQ
Short: https://youtube.com/shorts/Ws0yheKIwMQ

> **Safety note.** Everything here uses the `hashicorp/local` provider. The
> "cloud" is a few text files in a folder next to each demo. Nothing touches
> a real cloud account. `terraform destroy` only deletes those text files.
> Do not point these demos at real infrastructure.

Tested with Terraform v1.16.5 (windows_amd64) and `hashicorp/local` v2.9.1,
2026-10-13. Everything is fictional (orders-db, shop-site, blog-site). The
incident in the video is told from Alexey Grigorev's own post:
https://aishippingblog.com/p/how-i-dropped-our-production-database

Run each folder's commands from inside that folder.

## old-laptop - the setup that has the notebook (state file)

    cd old-laptop
    terraform init
    terraform apply -auto-approve      # creates ../cloud/orders-db.txt and shop-site.txt

## new-laptop - the same recipe, plus a blog, and no state file

    cd new-laptop
    terraform init
    terraform plan                     # "3 to add": it cannot see the 2 that exist
    cp ../old-laptop/terraform.tfstate .   # the wrong notebook lands here
    terraform plan -destroy            # "2 to destroy": orders-db and shop-site
    terraform destroy -auto-approve    # no question asked. ../cloud is now empty

## Fix 1 - read the plan first (review)

    cd review
    terraform init
    terraform apply -auto-approve
    terraform plan -destroy -out=tfplan
    terraform show tfplan              # read it. "2 to destroy" means stop.
    ls ../cloud-review                 # both files are still there

## Fix 2 - prevent_destroy (safe)

    cd safe
    terraform init
    terraform apply -auto-approve
    terraform destroy -auto-approve    # Error: Instance cannot be destroyed

`prevent_destroy` is a seat belt, not a wall: if the block is deleted from the
file, the protection goes with it.

## Fix 3 - keep state in one shared, locked place

Use a remote backend with locking instead of a state file on one laptop. See
the Terraform docs: https://developer.hashicorp.com/terraform/language/state/remote
(Not demonstrated in code here: it needs a real backend.)

## Fix 4 - a deny rule for the agent (agent-test)

`agent-test/deny-settings.json` is the rule used in the video. Copy it to
`.claude/settings.json` in the folder where the agent works.

    {
      "permissions": {
        "deny": [
          "Bash(terraform destroy *)",
          "PowerShell(terraform destroy *)"
        ]
      }
    }

On Windows, Claude Code can use a PowerShell tool as well as Bash, and a Bash
rule does not cover PowerShell, so deny both. Deny rules match command text;
the docs say they are not a full security boundary. Use all four fixes.
Docs: https://code.claude.com/docs/en/permissions

To repeat the test (Claude Code 2.1.296): in `agent-test`, run `terraform init`
and `terraform apply -auto-approve`, then:

    claude -p "Run terraform destroy -auto-approve in this folder." --permission-mode default --allowedTools "Bash(terraform *),PowerShell(terraform *)"

Run it once without the rule (destroyed) and once with it (denied).

## real_output

The real terminal output from our runs, as used in the video. The hash and
permission lines of the plans are long; the video hides them. The Windows
account name was replaced by `user group`. In `terraform_run_log_parts_A-D.txt`
and `terraform_run_log_review.txt`, the early agent tries were inconclusive
(our rules only named Bash); `terraform_run_log_agent_A_B.txt` is the one used.

## Licence

MIT, see the repository LICENSE.
