import ConfigParser


class ConfigLoader:
    def __init__(self, filename):
        cp = ConfigParser.ConfigParser()
        cp.read(filename)
        self.AWS_ACCESS_KEY_ID = cp.get("aws_s3", "AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = cp.get("aws_s3", "AWS_SECRET_ACCESS_KEY")
        self.bucketname = cp.get("aws_s3", "bucketname")
        self.mqtt_host = cp.get("mqtt","host")
        self.mqtt_id = cp.get("mqtt","id")
        self.mqtt_pub_topic = cp.get("mqtt","pub_topic")
        self.mqtt_sub_topic = cp.get("mqtt","sub_topic")
        self.imagesurl = cp.get("pattern", "listurl").split(",")
        self.imageid = cp.get("pattern", "listid").split(",")

def main():
    cl = ConfigLoader("configuration.ini")
if __name__ == "__main__":
    main()