from abc import ABC, abstractmethod


class VideoUrlParser(ABC):
    """Strategy interface for extracting video IDs from URLs."""

    @abstractmethod
    def extract_video_id(self, url: str) -> str | None:
        """Return the video ID if the URL is supported, otherwise None."""

    @abstractmethod
    def default_title(self, video_id: str) -> str:
        """Return a fallback title when none is provided."""
