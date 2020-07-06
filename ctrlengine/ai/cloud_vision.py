from google.cloud import vision
import cv2


class cloud_vision:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
        self.response = None
        self.faces = None
        self.props = None
        self.labels = None
        self.landmarks = None
        self.objects = None
        self.annotations = None
        self.texts = None

    def get_response(self):
        return self.response

    def get_faces(self):
        return self.face

    def get_props(self):
        return self.props

    def get_labels(self):
        return self.labels

    def get_landmarks(self):
        return self.landmarks

    def get_objects(self):
        return self.objects

    def get_annotations(self):
        return self.annotations

    def get_texts(self):
        return self.texts

    def __encode_image(self, image):
        ret, frame = cv2.imencode('.jpg', image)
        if ret != True:
            raise RuntimeException("Problem Encoding Image to .jpg")
        return vision.types.Image(content=frame.tostring())

    def detect_faces(self, image):
        image = self.__encode_image(image)
        self.response = self.client.face_detection(image=image)
        self.faces = self.response.face_annotations
        return self.faces

    def image_properties(self, image):
        image = self.__encode_image(image)
        self.response = self.client.image_properties(image=image)
        self.props = self.response.image_properties_annotation
        return self.props

    def detect_labels(self, image):
        image = self.__encode_image(image)
        self.response = self.client.label_detection(image=image)
        self.labels = self.response.label_annotations
        return self.labels

    def detect_landmarks(self, image):
        image = self.__encode_image(image)
        self.response = self.client.landmark_detection(image=image)
        self.landmarks = self.response.landmark_annotations
        return self.landmarks

    def detect_logos(self, image):
        image = self.__encode_image(image)
        self.response = self.client.logo_detection(image=image)
        self.logos = self.response.logo_annotations
        return self.logos

    def detect_objects(self, image):
        image = self.__encode_image(image)
        self.response = self.client.object_localization(image=image)
        self.objects = self.response.localized_object_annotations
        return self.objects

    def detect_web_entities(self, image):
        image = self.__encode_image(image)
        self.response = self.client.web_detection(image=image)
        self.annotations = self.response.web_detection
        return self.annotations

    def ocr(self, image):
        image = self.__encode_image(image)
        self.response = client.text_detection(image=image)
        self.texts = self.response.text_annotations
        return self.texts

    def ocr_handwriting(self, image):
        image = self.__encode_image(image)
        self.response = client.document_text_detection(image=image)
        self.texts = self.response.full_text_annotation
        return self.texts
