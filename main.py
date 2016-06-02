from RP.MotionSensor import *
from RP import *
from ImageUpload import *
from FaceDetection import *

#Template images id
imageIds = ["c594c66a-4442-4860-963a-ebc9a5d82ead"]

#AWS S3 Config
AWS_ACCESS_KEY_ID = 'AKIAIG7FK44VPPQHPO7A'
AWS_SECRET_ACCESS_KEY = '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'
bucketname = 'trung-aws-s3'


def main():
    sensor = Sensor(17)
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

        if imageUpload.upload_to_s3(file, key):
            print 'File uploaded'
        else:
            print 'File upload failed...'

        newImageURL = "http://sth.com/newfile.jpg"

        # Using MS API to compare

        fd = FaceDetection()
        fd.identifyFace(newImageURL)

        #MQTT Notify

        # sensor.waitFor(GPIO.FALLING);
        # print "Sensor is %d" % (sensor.getState())


if __name__ == "__main__":
    main()
