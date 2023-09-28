from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import numpy as np
from sklearn.cluster import KMeans
from typing import Tuple, List

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

app = FastAPI()

class ImageUrl(BaseModel):
    image_url: str

def load_image(path: str) -> Image.Image:
    try:
        if path.startswith(("http://", "https://")):
            response = requests.get(path)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Invalid URL")
            img = Image.open(BytesIO(response.content))
        else:
            img = Image.open(path)
        return img
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_palette(img: Image.Image, n_colors: int, resize_shape: Tuple[int, int] = (100, 100)) -> np.ndarray:
    img = img.convert("RGB")
    img = np.asarray(img.resize(resize_shape)) / 255.0
    h, w, c = img.shape
    img_arr = img.reshape(h * w, c)

    kmeans = KMeans(n_clusters=n_colors, n_init="auto").fit(img_arr)
    palette = (kmeans.cluster_centers_ * 255).astype(int)

    return palette

@app.post("/extract_colors/")
async def extract_colors(image_data: ImageUrl):
    try:
        url = image_data.image_url
        image = load_image(url)
        color_palette_rgb = get_palette(image, 6)  # Ekstrak 6 warna dominan
        color_palette_hex = [rgb_to_hex(tuple(color)) for color in color_palette_rgb]
        return JSONResponse(content={"warna_dominan": color_palette_hex})
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
