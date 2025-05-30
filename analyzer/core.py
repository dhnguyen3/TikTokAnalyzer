from dataclasses import dataclass
from typing import Dict, List
from .audio_analyzer import AudioAnalyzer
from .visual_analyzer import VisualAnalyzer

@dataclass
class AnalysisResult:
    score: float
    visual_metrics: Dict
    audio_metrics: Dict
    brand_consistency: Dict
    feedback: List[str]

class TikTokAnalyzer:
    def __init__(self):
        self.audio_analyzer = AudioAnalyzer()
        self.visual_analyzer = VisualAnalyzer()
    
    def analyze(self, video_path: str, reference_path: str) -> AnalysisResult:
        # Run analyses
        audio_analysis = self.audio_analyzer.analyze(video_path)
        visual_analysis = self.visual_analyzer.analyze(video_path)
        
        # Compare with reference (simplified)
        ref_analysis = self.visual_analyzer.analyze(reference_path)
        brightness_diff = abs(visual_analysis['brightness'] - ref_analysis['brightness'])
        
        # Generate score (0-100)
        score = max(0, 100 - brightness_diff * 2)
        if not visual_analysis['product_visible']:
            score -= 30
        
        # Generate feedback
        feedback = []
        if brightness_diff > 30:
            feedback.append("⚠️ Lighting differs significantly from reference")
        if not visual_analysis['product_visible']:
            feedback.append("❌ Product not clearly visible")
        
        return AnalysisResult(
            score=max(0, min(100, score)),
            visual_metrics=visual_analysis,
            audio_metrics=audio_analysis,
            brand_consistency={
                'mentions': audio_analysis.get('brand_mentions', []),
                'colors_present': visual_analysis['brand_colors_present']
            },
            feedback=feedback
        )