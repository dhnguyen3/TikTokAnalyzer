import cv2
import numpy as np
from typing import Dict, List

class VisualAnalyzer:
    def analyze(self, video_path: str) -> Dict:
        frames = self._extract_frames(video_path)
        
        return {
            'brightness': np.mean([self._get_brightness(f) for f in frames]),
            'contrast': np.mean([self._get_contrast(f) for f in frames]),
            'colorfulness': np.mean([self._get_colorfulness(f) for f in frames]),
            'product_visible': self._detect_products(frames),
            'brand_colors_present': self._detect_brand_colors(frames)
        }
    
    def _extract_frames(self, video_path: str, n_frames: int = 10) -> List[np.ndarray]:
        cap = cv2.VideoCapture(video_path)
        frames = []
        try:
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            for i in range(n_frames):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i * (total_frames // n_frames))
                ret, frame = cap.read()
                if ret:
                    frames.append(frame)
        finally:
            cap.release()
        return frames
    
    def _get_brightness(self, frame: np.ndarray) -> float:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return np.mean(gray)
    
    def _get_contrast(self, frame: np.ndarray) -> float:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return np.std(gray)
    
    def _get_colorfulness(self, frame: np.ndarray) -> float:
        (B, G, R) = cv2.split(frame.astype("float"))
        rg = np.absolute(R - G)
        yb = np.absolute(0.5 * (R + G) - B)
        std_root = np.sqrt((np.std(rg) ** 2) + (np.std(yb) ** 2))
        mean_root = np.sqrt((np.mean(rg) ** 2) + (np.mean(yb) ** 2))
        return std_root + (0.3 * mean_root)
    
    def _detect_products(self, frames: List[np.ndarray]) -> bool:
        """Placeholder for actual product detection"""
        return len(frames) > 0  # Dummy implementation
    
    def _detect_brand_colors(self, frames: List[np.ndarray]) -> bool:
        """Check for brand colors (yellow in this example)"""
        for frame in frames[:5]:  # Check first few frames
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])
            mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            if np.sum(mask) > 10000:
                return True
        return False