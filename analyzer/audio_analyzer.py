import whisper
import numpy as np
from typing import Dict

class AudioAnalyzer:
    def __init__(self):
        self.model = whisper.load_model("base")
    
    def analyze(self, video_path: str) -> Dict:
        # Transcribe audio
        result = self.model.transcribe(video_path)
        transcript = result["text"]
        
        # Simple brand mention detection
        brand_mentions = []
        if "brand" in transcript.lower():
            brand_mentions.append("brand")
        
        return {
            'transcript': transcript,
            'duration': result['segments'][-1]['end'] if result['segments'] else 0,
            'speech_rate': len(transcript.split()) / max(1, result['segments'][-1]['end']) if result['segments'] else 0,
            'brand_mentions': brand_mentions,
            'clarity_score': self._calculate_clarity(transcript)
        }
    
    def _calculate_clarity(self, text: str) -> float:
        """Simple clarity metric based on word count and punctuation"""
        word_count = len(text.split())
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        return min(10, word_count / max(1, sentence_count))