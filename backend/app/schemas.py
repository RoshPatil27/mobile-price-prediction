"""Pydantic models describing the API's request and response payloads."""

from pydantic import BaseModel, Field


class PhoneSpecs(BaseModel):
    """All 20 hardware specifications used by the trained model.

    Field constraints mirror the value ranges seen in the training data,
    so the interactive API docs (Swagger UI at /docs) double as a guide
    for valid input values.
    """

    battery_power: int = Field(..., ge=500, le=2000, description="Total energy capacity in mAh")
    blue: int = Field(..., ge=0, le=1, description="Has Bluetooth (1) or not (0)")
    clock_speed: float = Field(..., ge=0.5, le=3.0, description="Microprocessor clock speed in GHz")
    dual_sim: int = Field(..., ge=0, le=1, description="Has dual SIM support (1) or not (0)")
    fc: int = Field(..., ge=0, le=20, description="Front camera megapixels")
    four_g: int = Field(..., ge=0, le=1, description="Has 4G (1) or not (0)")
    int_memory: int = Field(..., ge=2, le=64, description="Internal memory in GB")
    m_dep: float = Field(..., ge=0.1, le=1.0, description="Mobile depth/thickness in cm")
    mobile_wt: int = Field(..., ge=80, le=200, description="Weight of the phone in grams")
    n_cores: int = Field(..., ge=1, le=8, description="Number of processor cores")
    pc: int = Field(..., ge=0, le=20, description="Primary camera megapixels")
    px_height: int = Field(..., ge=0, le=1960, description="Screen resolution height in pixels")
    px_width: int = Field(..., ge=500, le=1998, description="Screen resolution width in pixels")
    ram: int = Field(..., ge=256, le=4000, description="RAM in MB")
    sc_h: int = Field(..., ge=5, le=19, description="Screen height in cm")
    sc_w: int = Field(..., ge=0, le=18, description="Screen width in cm")
    talk_time: int = Field(..., ge=2, le=20, description="Longest single-charge talk time in hours")
    three_g: int = Field(..., ge=0, le=1, description="Has 3G (1) or not (0)")
    touch_screen: int = Field(..., ge=0, le=1, description="Has touch screen (1) or not (0)")
    wifi: int = Field(..., ge=0, le=1, description="Has WiFi (1) or not (0)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "battery_power": 1500,
                "blue": 1,
                "clock_speed": 2.2,
                "dual_sim": 1,
                "fc": 5,
                "four_g": 1,
                "int_memory": 32,
                "m_dep": 0.5,
                "mobile_wt": 150,
                "n_cores": 4,
                "pc": 10,
                "px_height": 800,
                "px_width": 1200,
                "ram": 2048,
                "sc_h": 13,
                "sc_w": 7,
                "talk_time": 10,
                "three_g": 1,
                "touch_screen": 1,
                "wifi": 1,
            }
        }
    }


class PredictionResponse(BaseModel):
    price_range: int = Field(..., description="Predicted class: 0-3")
    label: str = Field(..., description="Human-readable price tier")
    confidence: float = Field(..., description="Model confidence for the predicted class")
    probabilities: dict[str, float] = Field(..., description="Probability for every class")


class ModelInfoResponse(BaseModel):
    best_model: str
    results: dict
    class_labels: dict[str, str]
