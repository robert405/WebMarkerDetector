import base64
from PIL import Image
import io
import numpy as np

def readb64(imageData):

    head, data = imageData.split(',')
    imgdata = base64.b64decode(data)
    img = io.BytesIO(imgdata)
    img = Image.open(img)
    wsize = (int)(float(img.size[0]) / 2)
    hsize = (int)(float(img.size[1]) / 2)
    img = img.resize((wsize, hsize), Image.ANTIALIAS)
    img = np.asarray(img, dtype=np.uint8)

    return img