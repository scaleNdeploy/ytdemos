import boto3
from moto import mock_aws

BUCKET = "northridge-customer-reports"
AUTH_GROUP = ("http://acs.amazonaws.com/groups"
              "/global/AuthenticatedUsers")


def make_bucket(s3):
    s3.create_bucket(Bucket=BUCKET)
    s3.put_object(
        Bucket=BUCKET, Key="q3-report.csv",
        Body=b"account,total\n1001,4820\n1002,990\n")


def grant_authenticated_users(s3):
    """The mistake: someone reads 'Authenticated Users'
    as 'our own team'. AWS defines it as any AWS
    account holder, not our team."""
    s3.put_bucket_acl(
        Bucket=BUCKET,
        AccessControlPolicy={
            "Owner": {"ID": "northridge-owner"},
            "Grants": [{
                "Grantee": {"Type": "Group",
                            "URI": AUTH_GROUP},
                "Permission": "READ",
            }],
        },
    )


def show_grants(s3, label):
    acl = s3.get_bucket_acl(Bucket=BUCKET)
    print(label)
    for g in acl["Grants"]:
        who = g["Grantee"].get(
            "URI", g["Grantee"].get("ID"))
        print(" ", who, "->", g["Permission"])


def lock_it_down(s3):
    """The fix: block public access, and grant reads
    only to our own owner, not to any group."""
    s3.put_public_access_block(
        Bucket=BUCKET,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        },
    )
    s3.put_bucket_acl(
        Bucket=BUCKET,
        AccessControlPolicy={
            "Owner": {"ID": "northridge-owner"},
            "Grants": [{
                "Grantee": {"Type": "CanonicalUser",
                            "ID": "northridge-owner"},
                "Permission": "FULL_CONTROL",
            }],
        },
    )


@mock_aws
def main():
    s3 = boto3.client("s3", region_name="us-east-1")
    make_bucket(s3)
    grant_authenticated_users(s3)
    show_grants(s3, "Before the fix:")
    lock_it_down(s3)
    show_grants(s3, "After the fix:")
    pab = s3.get_public_access_block(Bucket=BUCKET)
    cfg = pab["PublicAccessBlockConfiguration"]
    print("Block public access:", cfg["BlockPublicAcls"])


main()
