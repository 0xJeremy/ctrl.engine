import requests
import os
import cv2

class azure_vision():
    FULL_ANALYSIS = 'Categories, Tags, Description, Faces'
    def __init__(self, api_key=None, api_endpoint=None):
        if api_key is None and 'AZURE_KEY' in os.environ:
            api_key = os.environ['AZURE_KEY']
        if api_endpoint is None and 'AZURE_ENDPOINT' in os.environ:
            api_endpoint = os.environ['AZURE_ENDPOINT']
        self.url = api_endpoint + "vision/v2.1/analyze"
        self.headers = {
            'Ocp-Apim-Subscription-Key': api_key,
            'Content-Type': 'application/octet-stream'
        }
        self.response = None
        self.analysis = None

    def __encode_image(self, image):
        ret, frame = cv2.imencode('.jpg', image)
        if(ret != True):
            raise RuntimeException("Problem Encoding Image to .jpg")
        return frame.tostring()

    def __run_analysis(self, image, params):
        image = self.__encode_image(image)
        params = {
            'visualFeatures': params
        }
        self.response = requests.post(
                    self.url, headers=self.headers, params=params, data=image)
        self.analysis = self.response.json()
        return self.analysis

    def analyze_image(self, image):
        return self.__run_analysis(image, self.FULL_ANALYSIS)

    def detect_faces(self, image):
        return self.__run_analysis(image, 'Faces')

    def analyze_categories(self, image):
        return self.__run_analysis(image, 'Categories')

    def analyze_description(self, image):
        return self.__run_analysis(image, 'Description')

    def analyze_tags(self, image):
        return self.__run_analysis(image, 'Tags')

    def analyze_brands(self, image):
        return self.__run_analysis(image, 'Brands')

    def custom_analysis(self, image, params):
        return self.__run_analysis(image, params)
