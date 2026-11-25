
import numpy as np
from PIL import Image
import io

reader = None


def extract_text_from_image(image_bytes: bytes) -> str:
    global reader

    if reader is None:
        import easyocr
        reader = easyocr.Reader(['en'], gpu=False)

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_array = np.array(image)

    results = reader.readtext(image_array)

    extracted_text = " ".join(
        result[1] for result in results
    )

    return extracted_text
