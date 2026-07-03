import re

from .base import VideoUrlParser

_YOUTUBE_PATTERNS = [
    re.compile(r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})"),
    re.compile(r"youtube\.com/shorts/([a-zA-Z0-9_-]{11})"),
]


class YouTubeUrlParser(VideoUrlParser):
    """Concrete strategy for YouTube karaoke URLs."""

    def extract_video_id(self, url: str) -> str | None:
        for pattern in _YOUTUBE_PATTERNS:
            match = pattern.search(url)
            if match:
                return match.group(1)
        return None

    def default_title(self, video_id: str) -> str:
        return f"YouTube · {video_id}"
