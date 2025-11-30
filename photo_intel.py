"""Photo Intelligence Module - Facial recognition and reverse image search."""
import os
import base64
import hashlib
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

class PhotoIntel:
    def __init__(self):
        self.services = {
            'google_images': 'https://www.google.com/searchbyimage',
            'yandex_images': 'https://yandex.com/images/search',
            'tineye': 'https://tineye.com/search',
            'bing_visual': 'https://www.bing.com/images/search'
        }
        self.upload_dir = 'uploads'
        os.makedirs(self.upload_dir, exist_ok=True)

    def collect(self, photo_path_or_url):
        """
        Perform photo intelligence gathering.
        Accepts either a local file path or a URL to an image.
        """
        print(f"[photo_intel] Starting photo analysis for: {photo_path_or_url}")
        results = []
        
        # Determine if input is URL or local file
        is_url = photo_path_or_url.startswith('http://') or photo_path_or_url.startswith('https://')
        
        if is_url:
            results.append({
                'type': 'image_source',
                'source': 'url',
                'url': photo_path_or_url,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            })
            image_hash = self._hash_from_url(photo_path_or_url)
        else:
            results.append({
                'type': 'image_source',
                'source': 'file',
                'path': photo_path_or_url,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            })
            image_hash = self._hash_from_file(photo_path_or_url)
        
        # Add image hash
        if image_hash:
            results.append({
                'type': 'image_hash',
                'algorithm': 'sha256',
                'hash': image_hash
            })
        
        # Reverse image search results (simulated)
        results.extend(self._reverse_image_search(photo_path_or_url, is_url))
        
        # Facial analysis (simulated)
        results.extend(self._facial_analysis())
        
        # EXIF data extraction (simulated)
        results.extend(self._extract_exif(photo_path_or_url, is_url))
        
        # Social media profile matching (simulated)
        results.extend(self._social_media_matching())
        
        print(f"[photo_intel] Analysis complete. Found {len(results)} data points")
        return results

    def _hash_from_file(self, file_path):
        """Calculate SHA256 hash of local file."""
        try:
            if not os.path.exists(file_path):
                return None
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            print(f"[photo_intel] Error hashing file: {e}")
            return None

    def _hash_from_url(self, url):
        """Calculate SHA256 hash from URL."""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return hashlib.sha256(response.content).hexdigest()
        except Exception as e:
            print(f"[photo_intel] Error hashing from URL: {e}")
        return None

    def _reverse_image_search(self, image_ref, is_url):
        """Simulate reverse image search across multiple platforms."""
        results = []
        
        # Google Images
        results.append({
            'platform': 'google_images',
            'service': 'Reverse Image Search',
            'search_url': f"{self.services['google_images']}?image_url={image_ref}" if is_url else self.services['google_images'],
            'matches_found': True,
            'estimated_matches': 847,
            'similar_images': 1203,
            'status': 'success'
        })
        
        # Yandex Images
        results.append({
            'platform': 'yandex_images',
            'service': 'Reverse Image Search',
            'search_url': self.services['yandex_images'],
            'matches_found': True,
            'estimated_matches': 523,
            'status': 'success'
        })
        
        # TinEye
        results.append({
            'platform': 'tineye',
            'service': 'Reverse Image Search',
            'search_url': self.services['tineye'],
            'matches_found': True,
            'estimated_matches': 156,
            'oldest_match': '2019-03-15',
            'newest_match': '2025-11-28',
            'status': 'success'
        })
        
        # Bing Visual Search
        results.append({
            'platform': 'bing_visual',
            'service': 'Visual Search',
            'search_url': self.services['bing_visual'],
            'matches_found': True,
            'estimated_matches': 692,
            'related_searches': ['person', 'profile photo', 'social media'],
            'status': 'success'
        })
        
        return results

    def _facial_analysis(self):
        """Simulate facial recognition and analysis."""
        return [
            {
                'type': 'facial_analysis',
                'faces_detected': 1,
                'confidence': 0.94,
                'attributes': {
                    'gender': 'male',
                    'age_range': '25-35',
                    'emotion': 'neutral',
                    'glasses': False,
                    'facial_hair': True
                },
                'face_quality': 'high',
                'face_landmarks': 68
            },
            {
                'type': 'facial_recognition',
                'database_matches': 3,
                'matches': [
                    {
                        'source': 'social_media',
                        'platform': 'linkedin',
                        'confidence': 0.87,
                        'match_type': 'possible'
                    },
                    {
                        'source': 'public_records',
                        'platform': 'gravatar',
                        'confidence': 0.92,
                        'match_type': 'likely'
                    },
                    {
                        'source': 'social_media',
                        'platform': 'facebook',
                        'confidence': 0.78,
                        'match_type': 'possible'
                    }
                ]
            }
        ]

    def _extract_exif(self, image_ref, is_url):
        """Simulate EXIF metadata extraction."""
        return [
            {
                'type': 'exif_data',
                'found': True,
                'camera_make': 'Apple',
                'camera_model': 'iPhone 13 Pro',
                'date_taken': '2025-11-15 14:23:17',
                'gps_coordinates': {
                    'latitude': 37.7749,
                    'longitude': -122.4194,
                    'location': 'San Francisco, CA'
                },
                'image_dimensions': {
                    'width': 3024,
                    'height': 4032
                },
                'software': 'iOS 17.1.2',
                'orientation': 'portrait'
            }
        ]

    def _social_media_matching(self):
        """Simulate social media profile matching."""
        return [
            {
                'type': 'social_media_match',
                'platform': 'instagram',
                'profile_found': True,
                'profile_url': 'https://instagram.com/user_profile',
                'match_confidence': 0.89,
                'profile_image_match': True,
                'followers': 1247,
                'posts': 342
            },
            {
                'type': 'social_media_match',
                'platform': 'facebook',
                'profile_found': True,
                'profile_url': 'https://facebook.com/user.profile',
                'match_confidence': 0.82,
                'profile_image_match': True,
                'friends_visible': False
            },
            {
                'type': 'social_media_match',
                'platform': 'twitter',
                'profile_found': True,
                'profile_url': 'https://twitter.com/userprofile',
                'match_confidence': 0.75,
                'profile_image_match': True,
                'verified': False,
                'followers': 523
            }
        ]

    def save_upload(self, file_data, filename):
        """Save uploaded photo file."""
        filepath = os.path.join(self.upload_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(file_data)
        return filepath
