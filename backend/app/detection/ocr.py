
import easyocr
import numpy as np
from PIL import Image
import io

# Initialize EasyOCR once when the module loads
reader = easyocr.Reader(['en'], gpu=False)


def extract_text_from_image(image_bytes: bytes) -> str:
    try:
        # Read image from uploaded bytes
        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")

        # Convert image into a NumPy array
        image_array = np.array(image)

        # Extract text using EasyOCR
        results = reader.readtext(
            image_array,
            detail=0,
            paragraph=True
        )

        # Combine extracted text
        extracted_text = " ".join(results)

        return extracted_text.strip()

    except Exception as error:
        raise ValueError(
            f"Unable to extract text from image: {error}"
        )
