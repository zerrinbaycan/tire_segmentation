import cv2
import typing
import numpy as np

def deepOCR(image):
    # pip install mltu==0.1.3
    from mltu.inferenceModel import OnnxInferenceModel
    from mltu.utils.text_utils import ctc_decoder, get_cer
    from mltu.configs import BaseModelConfigs

    class ImageToWordModel(OnnxInferenceModel):
        def __init__(self, char_list: typing.Union[str, list], *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.char_list = char_list

        def predict(self, image: np.ndarray):
            image = cv2.resize(image, self.input_shapes[0][1:3][::-1])

            image_pred = np.expand_dims(image, axis=0).astype(np.float32)

            preds = self.model.run(self.output_names, {self.input_names[0]: image_pred})[0]

            text = ctc_decoder(preds, self.char_list)[0]

            return text
        
    configs = BaseModelConfigs.load("deepOCR\Models/configs.yaml")
    model = ImageToWordModel(model_path='deepOCR\Models', char_list=configs.vocab)
    '''
    # Select ROI 
    r = cv2.selectROI("select the area", image) 

    # Crop image 
    cropped_image = image[int(r[1]):int(r[1]+r[3]),  
                          int(r[0]):int(r[0]+r[2])] 
    '''

    prediction_text = model.predict(image)
    return prediction_text

"""
prediction_text=deepOCR(cv2.imread(r"C:\\ZerrinGit\\CRAFT-pytorch\\result\\crop\\res_44__0.jpg"))
print("tahmin : {}".format(prediction_text)) 
"""
