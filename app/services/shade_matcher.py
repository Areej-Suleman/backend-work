from typing import List, Dict, Any
from PIL import Image
import io

class ShadeMatcherService:
    async def find_matching_shades(self, upload_file) -> List[Dict[str, Any]]:
        # Read bytes (works with Starlette UploadFile)
        data = await upload_file.read()
        # Example: inspect average color (placeholder)
        try:
            img = Image.open(io.BytesIO(data)).convert("RGB")
            w, h = img.size
            pixels = list(img.getdata())
            r = sum(p[0] for p in pixels) // len(pixels)
            g = sum(p[1] for p in pixels) // len(pixels)
            b = sum(p[2] for p in pixels) // len(pixels)
            avg_hex = f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            avg_hex = "#aaaaaa"
        # Return dummy shade matches
        return [
            {"brand": "Generic", "product": "Tinted Moisturizer", "shade": "Medium", "approx_hex": avg_hex},
            {"brand": "Generic", "product": "Foundation", "shade": "Beige", "approx_hex": avg_hex},
        ]
