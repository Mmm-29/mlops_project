import os,sys

class s3sync:
    def sync_folder_to_s3(self,folder,aws_bucket_url):
        """
        Syncs a local folder to an S3 bucket.
        
        :param folder: Local folder path to sync.
        :param aws_bucket_url: S3 bucket URL where the folder will be synced.
        """
        command="aws s3 sync {} {}".format(folder, aws_bucket_url)
        os.system(command)

    def sync_folder_from_s3(self,aws_bucket_url,folder):
        """
        Syncs an S3 bucket to a local folder.
        
        :param aws_bucket_url: S3 bucket URL to sync from.
        :param folder: Local folder path where the S3 bucket will be synced.
        """
        command="aws s3 sync {} {}".format(aws_bucket_url, folder)
        os.system(command)


