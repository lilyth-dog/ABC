"""
TESS Dataset Loader for Digital Human Twin
Toronto Emotional Speech Set (TESS) - Emotion Recognition

Features:
- Load and preprocess audio files
- Extract emotion labels from filenames
- Compatible with the BehavioralPersonalityDecoder
"""
import os
import json
import random
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import wave
import struct


# Emotion mapping from TESS dataset
EMOTION_LABELS = {
    'angry': {'valence': -0.7, 'arousal': 0.8, 'personality_weight': {'neuroticism': 0.3}},
    'disgust': {'valence': -0.6, 'arousal': 0.2, 'personality_weight': {'neuroticism': 0.2, 'agreeableness': -0.2}},
    'fear': {'valence': -0.8, 'arousal': 0.7, 'personality_weight': {'neuroticism': 0.4}},
    'happy': {'valence': 0.9, 'arousal': 0.6, 'personality_weight': {'extraversion': 0.3, 'openness': 0.2}},
    'neutral': {'valence': 0.0, 'arousal': 0.0, 'personality_weight': {}},
    'ps': {'valence': 0.7, 'arousal': 0.8, 'personality_weight': {'openness': 0.3}},  # Pleasant Surprise
    'sad': {'valence': -0.7, 'arousal': -0.3, 'personality_weight': {'neuroticism': 0.2}},
}


class TESSDataLoader:
    """
    Loader for Toronto Emotional Speech Set (TESS) dataset.
    
    Dataset structure:
    tess/
    ├── TESS Toronto emotional speech set data/
    │   ├── OAF_angry/
    │   │   ├── OAF_back_angry.wav
    │   │   └── ...
    │   ├── OAF_disgust/
    │   ├── OAF_fear/
    │   ├── OAF_happy/
    │   ├── OAF_neutral/
    │   ├── OAF_ps/
    │   ├── OAF_sad/
    │   ├── YAF_angry/
    │   └── ... (14 folders total)
    """
    
    def __init__(self, dataset_path: str = None):
        """Initialize loader with dataset path."""
        if dataset_path is None:
            # Default path relative to backend
            base_path = Path(__file__).parent.parent
            dataset_path = base_path / "datasets" / "tess" / "TESS Toronto emotional speech set data"
        
        self.dataset_path = Path(dataset_path)
        self.samples: List[Dict] = []
        self._loaded = False
    
    def load(self) -> int:
        """
        Load all samples from the dataset.
        
        Returns:
            Number of samples loaded
        """
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")
        
        self.samples = []
        
        # Iterate through emotion folders
        for folder in self.dataset_path.iterdir():
            if folder.is_dir():
                # Parse folder name: OAF_angry, YAF_happy, etc.
                parts = folder.name.split('_')
                if len(parts) >= 2:
                    actor = parts[0]  # OAF (Older Actor Female) or YAF (Younger Actor Female)
                    emotion = parts[1].lower()
                    
                    if emotion in EMOTION_LABELS:
                        # Load all wav files in this folder
                        for audio_file in folder.glob("*.wav"):
                            sample = {
                                'path': str(audio_file),
                                'actor': actor,
                                'emotion': emotion,
                                'word': audio_file.stem.split('_')[1] if '_' in audio_file.stem else '',
                                'emotion_data': EMOTION_LABELS[emotion]
                            }
                            self.samples.append(sample)
        
        self._loaded = True
        return len(self.samples)
    
    def get_sample(self, index: int) -> Dict:
        """Get a specific sample by index."""
        if not self._loaded:
            self.load()
        return self.samples[index]
    
    def get_random_samples(self, n: int = 10, emotion: Optional[str] = None) -> List[Dict]:
        """
        Get random samples, optionally filtered by emotion.
        
        Args:
            n: Number of samples to return
            emotion: Optional emotion filter
            
        Returns:
            List of sample dictionaries
        """
        if not self._loaded:
            self.load()
        
        pool = self.samples
        if emotion:
            pool = [s for s in self.samples if s['emotion'] == emotion]
        
        return random.sample(pool, min(n, len(pool)))
    
    def get_emotion_distribution(self) -> Dict[str, int]:
        """Get count of samples per emotion."""
        if not self._loaded:
            self.load()
        
        distribution = {}
        for sample in self.samples:
            emotion = sample['emotion']
            distribution[emotion] = distribution.get(emotion, 0) + 1
        
        return distribution
    
    def get_audio_features(self, audio_path: str) -> Dict:
        """
        Extract basic audio features from a WAV file.
        
        Args:
            audio_path: Path to WAV file
            
        Returns:
            Dictionary with audio features
        """
        with wave.open(audio_path, 'rb') as wav:
            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            framerate = wav.getframerate()
            n_frames = wav.getnframes()
            duration = n_frames / framerate
            
            # Read raw audio data
            raw_data = wav.readframes(n_frames)
            
            # Convert to samples
            if sample_width == 2:
                fmt = f'<{n_frames * channels}h'
                samples = struct.unpack(fmt, raw_data)
            else:
                samples = raw_data
            
            # Calculate basic features
            if samples:
                max_amplitude = max(abs(s) for s in samples) if isinstance(samples[0], int) else 0
                avg_amplitude = sum(abs(s) for s in samples) / len(samples) if isinstance(samples[0], int) else 0
            else:
                max_amplitude = 0
                avg_amplitude = 0
        
        return {
            'channels': channels,
            'sample_rate': framerate,
            'duration': duration,
            'max_amplitude': max_amplitude,
            'avg_amplitude': avg_amplitude,
        }
    
    def to_behavioral_profile(self, sample: Dict) -> Dict:
        """
        Convert a TESS sample to a behavioral profile format
        compatible with BehavioralPersonalityDecoder.
        
        Args:
            sample: TESS sample dictionary
            
        Returns:
            Behavioral profile dictionary
        """
        emotion_data = sample['emotion_data']
        
        # Map emotion to behavioral metrics
        valence = emotion_data['valence']
        arousal = emotion_data['arousal']
        
        # Convert to behavioral metrics
        profile = {
            'pathEfficiency': 0.5 + (valence * 0.3),  # Higher valence = more efficient
            'avgDecisionLatency': 2000 + (arousal * -500),  # Higher arousal = faster decisions
            'revisionRate': max(0, int(2 - valence)),  # Negative valence = more revisions
            'jitterIndex': max(0, arousal * 0.3),  # Arousal affects jitter
            'intensity': 0.5 + (arousal * 0.3),
            'emotionalContext': {
                'detected_emotion': sample['emotion'],
                'valence': valence,
                'arousal': arousal,
            },
            'contextualChoices': {
                'emotionSource': 'audio_analysis'
            }
        }
        
        return profile
    
    def export_metadata(self, output_path: str) -> str:
        """
        Export dataset metadata to JSON format for frontend use.
        
        Args:
            output_path: Path to save JSON file
            
        Returns:
            Path to saved file
        """
        if not self._loaded:
            self.load()
        
        metadata = {
            'dataset': 'TESS',
            'description': 'Toronto Emotional Speech Set',
            'total_samples': len(self.samples),
            'emotions': list(EMOTION_LABELS.keys()),
            'emotion_distribution': self.get_emotion_distribution(),
            'emotion_mappings': EMOTION_LABELS,
            'actors': ['OAF', 'YAF'],
            'actor_descriptions': {
                'OAF': 'Older Actor Female (64 years)',
                'YAF': 'Younger Actor Female (26 years)'
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return output_path


# Convenience function
def load_tess_dataset(dataset_path: str = None) -> TESSDataLoader:
    """
    Convenience function to load TESS dataset.
    
    Args:
        dataset_path: Optional custom path to dataset
        
    Returns:
        Loaded TESSDataLoader instance
    """
    loader = TESSDataLoader(dataset_path)
    loader.load()
    return loader


if __name__ == '__main__':
    # Test the loader
    import sys
    
    # Find dataset path
    script_dir = Path(__file__).parent
    dataset_path = script_dir.parent / "datasets" / "tess" / "TESS Toronto emotional speech set data"
    
    print(f"Loading TESS dataset from: {dataset_path}")
    
    try:
        loader = TESSDataLoader(str(dataset_path))
        count = loader.load()
        print(f"✅ Loaded {count} samples")
        
        print("\n📊 Emotion Distribution:")
        for emotion, count in loader.get_emotion_distribution().items():
            print(f"  {emotion}: {count}")
        
        print("\n🎯 Random Sample:")
        sample = loader.get_random_samples(1)[0]
        print(f"  File: {sample['path']}")
        print(f"  Actor: {sample['actor']}")
        print(f"  Emotion: {sample['emotion']}")
        
        print("\n🔄 Converted to Behavioral Profile:")
        profile = loader.to_behavioral_profile(sample)
        for key, value in profile.items():
            print(f"  {key}: {value}")
        
        # Export metadata
        metadata_path = script_dir / "tess_metadata.json"
        loader.export_metadata(str(metadata_path))
        print(f"\n📁 Metadata exported to: {metadata_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
