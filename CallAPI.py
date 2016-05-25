import httplib
import urllib


class FaceDetection:
    def __init__(self, apiUrl = "https://api.projectoxford.ai/face/v1.0", key = "d2495e1c650941ecbf2598373f5243c4"):
        self.apiKey = key
        self.apiUrl = apiUrl
        self.imagesPatternId = ["faceid1", "faceid2", "faceid3"]

    def getFaceId(self, imageUrl):
        param = {
            "returnFaceId": True,
        }
        body = {"url": imageUrl}
        method = "/detect"
        returnData = self.sendHTTPSRequest(param, method, body)
        print returnData

    def compare2Faces(self, imagesId):
        param = "{}"
        body = "{}"
        method = "/verify"
        returnData = self.sendHTTPSRequest(param, method, body)

    def sendHTTPSRequest(self, param, method, body):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.apiKey
        }

        params = urllib.urlencode(param)

        try:
            conn = httplib.HTTPSConnection(self.apiUrl)
            conn.request("POST", "%s?%s" % (method, params), body, headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
            return data
        except Exception as e:
            print("[Error {0}] {1}".format(e.message, e.message))
        return ""

def main():
    fd = FaceDetection()
    imageUrl = "https://www2.rsna.org/timssnet/media/pressreleases/images/Rybicki2-lg.jpg"
    fd.getFaceId(imageUrl)

if __name__ == "__main__":
    main()


