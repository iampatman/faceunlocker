from RP.MotionSensor import *
from RP import *
from ImageUpload import *
from FaceDetection import *
from MQTT_Publisher import *
#Template images id
imageIds = ["c594c66a-4442-4860-963a-ebc9a5d82ead"]
imageUrls = []
#AWS S3 Config
AWS_ACCESS_KEY_ID = 'x'
AWS_SECRET_ACCESS_KEY = 'x'
bucketname = 'trung-aws-s3'


def main():
    sensor = Sensor(17)
    print ("start face detector")
    fd = FaceDetection()
    print ("starting done")
    mqtt = MQTT_Center(host="dkiong.no-ip.biz",pubid="myid")
    while True:
        sensor.waitFor(GPIO.RISING);
        print "Sensor is %d" % (sensor.getState())

        lcd = Lcd()
        lcd.clear()
        lcd.display_string("Capturing in: ", 1)
        lcd.display_string("seconds", 3)
        i = 1
        for i in range(1, 5, 1):
            time.sleep(1)
            lcd.display_string(i, 2)

        # Capture picture function returns path to the new picture

        filePath = "newfile.jpg"

        # Upload to S3
        file = open(filePath, 'r+')

        key = file.name

        imageUpload = ImageUpload(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                  bucketname=bucketname)
        newImageURL = "https://s3-ap-northeast-1.amazonaws.com/trung-aws-s3/test1.jpg"
        newImageURL = imageUpload.upload_to_s3(file, key)
        if newImageURL != "":
            print 'File uploaded'
        else:
            print 'File upload failed...'


        # Using MS API to compare

        confidence = fd.identifyFace(newImageURL)

        #MQTT Notify

        if confidence < 0.5:
            mqtt.publish(topic="trung", message=newImageURL)

        else:
            #Open the door, display welcome message
        # sensor.waitFor(GPIO.FALLING);
        # print "Sensor is %d" % (sensor.getState())


if __name__ == "__main__":
    main()
