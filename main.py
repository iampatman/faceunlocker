from ImageUpload import *
from FaceDetection import *
from MQTTCenter import *
from ConfigLoader import *
# from RP.Sensor import *
# from RP.LCDDisplay import import *


# Template images id



def main():

    sensor = Sensor(17)
    config = ConfigLoader("config//development.ini")
    print ("start face detector")
    fd = FaceDetection(patternIds=config.imageid, patternUrls=config.imagesurl)
    print ("starting done")
    lcd = Lcd()
    mqtt = MQTTCenter(host=config.mqtt_host, pubid=config.mqtt_id)
    while True:

        sensor.waitFor(GPIO.RISING);
        print "Sensor is %d" % (sensor.getState())

        lcd.clear()
        lcd.display_string("Capturing in: ", 1)
        lcd.display_string("seconds", 3)
        i = 1
        for i in range(1, 5, 1):
            time.sleep(1)
            lcd.display_string(i, 2)

        # Capture picture function returns path to the new picture

        # Ankan: write your function and use it here, assign the return path into the filePath variable
        filePath = raw_input("Type in the file name: ")
        # filePath = "images//ramsey.jpg"
        key = filePath
        # Upload to S3
        filePath = "images//%s" % (filePath)
        file = open(filePath, 'r+')

        # key = file.name.split("//")[1]

        imageUpload = ImageUpload(aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                                  bucketname=config.bucketname)
        print ("Uploading file")
        newImageURL = imageUpload.upload_to_s3(file, key)
        if newImageURL != "":
            print 'File uploaded'
        else:
            print 'File upload failed...'
        # Using MS API to compare
        confidence = fd.identifyFace(newImageURL)
        print ("Confidence: " + str(confidence))

        # MQTT Notify
        if confidence < 0:
            print ("fake images")
        elif confidence < 1:
            print (time.time())
            mqtt.publish(topic="askforpermission", message=newImageURL)
            while mqtt.currentKey != "":
                mqtt.client.loop()
        else:
            print ("Door opened")
                mqtt.opendoor()

            # Open the door, display welcome message
            # sensor.waitFor(GPIO.FALLING);
            # print "Sensor is %d" % (sensor.getState())


if __name__ == "__main__":
    main()
