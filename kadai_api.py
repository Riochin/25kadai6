"""FastAPI application for data analysis and visualization.

This module provides endpoints for trendline calculation and image generation
using the functions defined in kadai_functions.
"""
import os
from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from kadai_functions import country_trendline, fit_trendline, generate_image

app = FastAPI()


@app.get("/say_hi/")
def say_hi():
    """Return a simple greeting message."""
    return {"Hi": "There"}


@app.get("/say_hello/{name}")
def say_hello(name):
    """Return a personalized greeting message."""
    return {"Hello": name}


class TrendlineInput(BaseModel):
    """Input model for trendline calculation with timestamps and data points."""
    timestamps: List[int]
    data: List[float]


@app.post(
    "/fit_trendline/",
    summary="Fit a trendline to any data",
    description="Provide a list of integer timestamps and a list of floats",
)
def calculate_trendline(trendline_input: TrendlineInput):
    """Calculate trendline slope and R-squared for given data points."""
    slope, r_squared, _ = fit_trendline(trendline_input.timestamps, trendline_input.data)
    return {"slope": slope, "r_squared": r_squared}


@app.get("/country_trendline/{country}")
def calculate_country_trendline(country: str):
    """Calculate trendline for a specific country's data."""
    slope, r_squared, _ = country_trendline(country)
    return {"slope": slope, "r_squared": r_squared}


@app.get("/country_image/{country}")
def generate_country_image(country: str):
    """Generate and return an image for a specific country."""
    image_path = generate_image(country)
    # image_path = country+".png"
    print(image_path)
    if os.path.exists(image_path):
        return FileResponse(image_path, media_type="image/png")
    return {"error": "画像生成に失敗しました"}

@app.get("/say_bye/{name}")
def say_bye(name):
    """Return a personalized goodbye message."""
    return {"Bye": name}