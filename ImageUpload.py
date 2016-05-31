import os
import boto
from boto.s3.key import Key

class ImageUpload:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucketname):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.bucketname = bucketname


    def upload_to_s3(self, file, key, callback=None, md5=None, reduced_redundancy=False, content_type=None):
        try:
            size = os.fstat(file.fileno()).st_size
        except:
            # Not all file objects implement fileno(),
            # so we fall back on this
            file.seek(0, os.SEEK_END)
            size = file.tell()
        conn = boto.connect_s3(self.aws_access_key_id, self.aws_secret_access_key)
        bucket = conn.get_bucket(self.bucketname, validate=False)
        k = Key(bucket)
        k.key = key
        #k.set_acl(acl_str='public-read', headers='test1.jpg')
        if content_type:
            k.set_metadata('Content-Type', content_type)
        sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy, rewind=False)

    # Rewind for later use
        file.seek(0)

        if sent == size:
            return True
        return False


def main():
    AWS_ACCESS_KEY_ID = 'AKIAIG7FK44VPPQHPO7A'
    AWS_SECRET_ACCESS_KEY = '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'

    file = open('test1.jpg', 'r+')

    key = file.name
    bucketname = 'trung-aws-s3'

    imageUpload = ImageUpload(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                              bucketname=bucketname)

    if imageUpload.upload_to_s3(file, key):
        print 'It worked!'
    else:
        print 'The upload failed...'

if __name__ == "__main__":
    main()

