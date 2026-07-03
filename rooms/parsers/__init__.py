from .base import VideoUrlParser
from .youtube import YouTubeUrlParser

_default_parser = YouTubeUrlParser()


def get_video_url_parser() -> VideoUrlParser:
    return _default_parser
