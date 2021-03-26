from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage


class PrivateMediaStorage(S3Boto3Storage):
    """
    In order to use this storage, in the file
    df_20210326/utils/terraform/variables.tf
    change the `s3_media_bucket_is_public` setting in Terraform to false
    """

    location = settings.MEDIAFILES_LOCATION
    default_acl = "private"


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    default_acl = "public-read"
