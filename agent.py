from dataclasses import dataclass
from typing import Any

from PIL import Image

from utils.groq_helper import generate_fallback_report, generate_report
from utils.leaf_check import is_leaf_image
from utils.predict import predict_disease


@dataclass
class DiagnosisResult:
    model_result: dict[str, Any]
    report: dict[str, Any]
    report_warning: str | None = None


def diagnose_leaf_image(image: Image.Image) -> DiagnosisResult:
    """Validate a leaf image, predict disease, and generate the care report."""
    if not is_leaf_image(image):
        raise ValueError("Please upload a valid leaf image")

    model_result = predict_disease(image)
    disease_name = model_result["disease_name"]
    plant_name = model_result["plant_name"]
    confidence_percent = round(float(model_result["confidence"]), 2)

    try:
        report = generate_report(
            disease_name=disease_name,
            confidence=confidence_percent,
            plant_name=plant_name,
            model_outputs=model_result,
        )
        return DiagnosisResult(model_result=model_result, report=report)
    except Exception as exc:
        report = generate_fallback_report(
            disease_name=disease_name,
            confidence=confidence_percent,
            plant_name=plant_name,
            model_outputs=model_result,
        )
        return DiagnosisResult(
            model_result=model_result,
            report=report,
            report_warning=f"Groq report could not be generated, so a local report was created instead: {exc}",
        )
