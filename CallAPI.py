import httplib
import json
import urllib


class FaceDetection:
    def __init__(self, apiUrl="api.projectoxford.ai", key="d2495e1c650941ecbf2598373f5243c4"):
        self.apiKey = key
        self.apiUrl = apiUrl
        self.imagesPatternId = ["c594c66a-4442-4860-963a-ebc9a5d82ead"]

    def getFaceId(self, imageUrl):
        param = {
            "returnFaceId": True,
        }
        body = {"url": imageUrl}
        method = "/face/v1.0/detect"
        returnData = self.sendHTTPSRequest(param, method, body)
        faceId = ""
        if not returnData == "":
            dict = returnData[0]
            faceId = dict['faceId']
        print faceId
        return faceId

    def compare2Faces(self, imageId1, imageId2):
        param = {}
        body = {
            "faceId1": imageId1,
            "faceId2": imageId2
        }
        method = "/face/v1.0/verify"
        returnData = self.sendHTTPSRequest(param, method, body)
        isIdentical = returnData["isIdentical"]
        result = 0
        if isIdentical:
            result = returnData["confidence"]
        print result
        return result

    def identifyFace(self, imageUrl):
        faceId = self.getFaceId(imageUrl)
        for imageId in self.imagesPatternId:
            result = self.compare2Faces(faceId, imageId)
            print result

    def sendHTTPSRequest(self, param, method, body):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.apiKey
        }
        params = urllib.urlencode(param)
        try:
            conn = httplib.HTTPSConnection(self.apiUrl)
            print "Log: Start sending http request to URL: "
            conn.request("POST", "%s?%s" % (method, params), json.dumps(body), headers)
            response = conn.getresponse()
            print "Log: Got result from URL"
            data = response.read()
            # Validate the received data to see whether it is in json format


            dict = json.loads(data)
            print "Log: Result %s" % dict
            conn.close()
            return dict
        except Exception as e:
            print("[Error {0}] {1}".format(e.message, e.message))
        return ""


def main():
    imageIds = ["c594c66a-4442-4860-963a-ebc9a5d82ead"]
    fd = FaceDetection()
    imageUrl = "https://www2.rsna.org/timssnet/media/pressreleases/images/Rybicki2-lg.jpg"
    fd.identifyFace(imageUrl)


if __name__ == "__main__":
    main()
