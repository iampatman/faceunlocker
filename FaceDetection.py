import httplib
import json
import urllib


class FaceDetection:
    def __init__(self, apiUrl="api.projectoxford.ai", key="d2495e1c650941ecbf2598373f5243c4", patternIds=[],
                 patternUrls=[]):
        self.apiKey = key
        self.apiUrl = apiUrl
        self.patternUrls = patternUrls
        self.imagesPatternId = patternIds
        if len(self.patternUrls) > 0:
            for url in self.patternUrls:
                newfaceid = self.getFaceId(url)
                self.imagesPatternId.append(newfaceid)

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
        if returnData.__contains__("error"):
            return 0
        isIdentical = returnData["isIdentical"]
        result = 0
        if isIdentical:
            result = returnData["confidence"]
        print result
        return result

    def identifyFace(self, imageUrl):
        faceId = self.getFaceId(imageUrl)
        maxConfidence = 0
        for imageId in self.imagesPatternId:
            result = self.compare2Faces(faceId, imageId)
            print result
            if result > maxConfidence:
                maxConfidence = result
        return maxConfidence

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
   # imageIds = ["c3f9600c-1871-45e1-81d3-d60c0fef5753"]

    imageUrls = ["https://arsenalfrenchclub.files.wordpress.com/2013/08/tumblr_mr95bnvm3s1qfj1xoo4_1280.jpg"]
    fd = FaceDetection(patternUrls=imageUrls)
    imageUrl = "http://www.aitonline.tv/pix/NewsImages/12657.jpg"
    result = fd.identifyFace(imageUrl)
    print "result: %f" % result


if __name__ == "__main__":
    main()
