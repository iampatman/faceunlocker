from ImageUpload import *
from FaceDetection import *
from MQTT_Publisher import *
from ConfigLoader import *


# Template images id
# imageIds = ["c594c66a-4442-4860-963a-ebc9a5d82ead"]
# imageUrls = []


def main():
    #sensor = Sensor(17)
    config = ConfigLoader("config//development.ini")
    print ("start face detector")
    fd = FaceDetection(patternIds=config.imageid, patternUrls=config.imagesurl)
    print ("starting done")
    mqtt = MQTT_Center(host=config.mqtt_host, pubid=config.mqtt_id)
    while True:
        # sensor.waitFor(GPIO.RISING);
        # print "Sensor is %d" % (sensor.getState())
        # lcd = Lcd()
        # lcd.clear()
        # lcd.display_string("Capturing in: ", 1)
        # lcd.display_string("seconds", 3)
        # i = 1
        # for i in range(1, 5, 1):
        #     time.sleep(1)
        #     lcd.display_string(i, 2)

        # Capture picture function returns path to the new picture

        # Ankan: write your function and use it here, assign the return path into the filePath variable
        filePath = ".jpg"

        # Upload to S3
        file = open(filePath, 'r+')

        key = file.name

        imageUpload = ImageUpload(aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                                  bucketname=config.bucketname)
        newImageURL = "https://s3-ap-northeast-1.amazonaws.com/trung-aws-s3/test1.jpg"
        newImageURL = imageUpload.upload_to_s3(file, key)
        if newImageURL != "":
            print 'File uploaded'
        else:
            print 'File upload failed...'

        # Using MS API to compare

        confidence = fd.identifyFace(newImageURL)
        print (confidence)

        # MQTT Notify

        if confidence < 0.5:
            print (time.time())
            mqtt.publish(topic="trung", message=newImageURL)

    # Open the door, display welcome message
    # sensor.waitFor(GPIO.FALLING);
    # print "Sensor is %d" % (sensor.getState())



if __name__ == "__main__":
    main()
