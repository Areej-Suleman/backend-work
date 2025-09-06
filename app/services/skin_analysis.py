from typing import Dict, List, Optional, Any
import cv2
import numpy as np
from PIL import Image
import io

class SkinAnalysisService:
    def __init__(self):
        self.skin_types = ["oily", "dry", "combination", "sensitive", "normal"]
        self.skin_concerns = ["acne", "wrinkles", "dark_spots", "redness", "dullness"]

    async def analyze_skin_image(self, image_data: bytes) -> Dict[str, Any]:
        """Analyze skin from uploaded image"""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Basic skin analysis (placeholder implementation)
            analysis_result = {
                "skin_type": self._detect_skin_type(opencv_image),
                "skin_tone": self._detect_skin_tone(opencv_image),
                "concerns": self._detect_skin_concerns(opencv_image),
                "moisture_level": self._analyze_moisture(opencv_image),
                "oil_level": self._analyze_oil_level(opencv_image),
                "recommendations": []
            }
            
            # Generate recommendations based on analysis
            analysis_result["recommendations"] = self._generate_recommendations(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    def _detect_skin_type(self, image: np.ndarray) -> str:
        """Detect skin type from image"""
        # Placeholder implementation - in reality would use ML models
        # For now, return a random skin type
        import random
        return random.choice(self.skin_types)

    def _detect_skin_tone(self, image: np.ndarray) -> Dict[str, Any]:
        """Detect skin tone and undertone"""
        # Calculate average color in face region
        height, width = image.shape[:2]
        center_region = image[height//4:3*height//4, width//4:3*width//4]
        
        avg_color = np.mean(center_region, axis=(0, 1))
        
        return {
            "rgb": [int(avg_color[2]), int(avg_color[1]), int(avg_color[0])],
            "hex": f"#{int(avg_color[2]):02x}{int(avg_color[1]):02x}{int(avg_color[0]):02x}",
            "undertone": self._determine_undertone(avg_color)
        }

    def _determine_undertone(self, avg_color: np.ndarray) -> str:
        """Determine skin undertone"""
        r, g, b = avg_color[2], avg_color[1], avg_color[0]
        
        if r > g and r > b:
            return "warm"
        elif b > r and b > g:
            return "cool"
        else:
            return "neutral"

    def _detect_skin_concerns(self, image: np.ndarray) -> List[str]:
        """Detect skin concerns"""
        # Placeholder implementation
        import random
        return random.sample(self.skin_concerns, random.randint(1, 3))

    def _analyze_moisture(self, image: np.ndarray) -> int:
        """Analyze moisture level (0-100)"""
        # Placeholder implementation
        import random
        return random.randint(30, 90)

    def _analyze_oil_level(self, image: np.ndarray) -> int:
        """Analyze oil level (0-100)"""
        # Placeholder implementation
        import random
        return random.randint(20, 80)

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate skincare recommendations based on analysis"""
        recommendations = []
        
        skin_type = analysis.get("skin_type", "normal")
        concerns = analysis.get("concerns", [])
        
        if skin_type == "oily":
            recommendations.append("Use oil-free moisturizer")
            recommendations.append("Consider salicylic acid cleanser")
        elif skin_type == "dry":
            recommendations.append("Use hydrating serum")
            recommendations.append("Apply rich moisturizer twice daily")
        elif skin_type == "sensitive":
            recommendations.append("Use fragrance-free products")
            recommendations.append("Patch test new products")
        
        if "acne" in concerns:
            recommendations.append("Consider benzoyl peroxide treatment")
        if "wrinkles" in concerns:
            recommendations.append("Use retinol products")
        if "dark_spots" in concerns:
            recommendations.append("Apply vitamin C serum")
        
        return recommendations

# Global skin analysis service instance
skin_analysis_service = SkinAnalysisService()
