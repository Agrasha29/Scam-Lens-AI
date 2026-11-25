import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.detection.detector import analyze_message, analyze_url
from fastapi import UploadFile, File
from app.detection.ocr import extract_text_from_image



app = FastAPI(
    title="ScamLens API",
    description="Suspicious Message Analysis System",
    version="1.0.0"
)

frontend_origin = os.getenv(
    "FRONTEND_ORIGIN",
    "http://127.0.0.1:5500"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        frontend_origin
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageRequest(BaseModel):
    message: str
class URLRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {
        "message": "Welcome to ScamLens API!",
        "status": "Running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze")
def analyze(request: MessageRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a message to analyze."
        )

    result = analyze_message(request.message)

    return result

@app.post("/analyze-url")
def analyze_url_endpoint(request: URLRequest):

    if not request.url.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a URL to analyze."
        )

    return analyze_url(request.url)


@app.post("/analyze-image")
async def analyze_image_endpoint(
    file: UploadFile = File(...)
):
    allowed_types = ["image/jpeg", "image/png"]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG or PNG image."
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty."
        )

    if len(image_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="Image size must be less than 5 MB."
        )

    try:
        extracted_text = extract_text_from_image(image_bytes)

        if not extracted_text:
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the screenshot."
            )

        result = analyze_message(extracted_text)

        return {
            "extracted_text": extracted_text,
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "detected_indicators": result["detected_indicators"],
            "recommendations": result["recommendations"],
            "ml_prediction": result["ml_prediction"],
            "ml_spam_probability": result["ml_spam_probability"]
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Screenshot analysis failed."
        )

    finally:
        await file.close()
