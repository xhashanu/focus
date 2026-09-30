import logging
import os
import shutil
import uuid
from pathlib import Path
from typing import List, Tuple
from app.config import settings

logger = logging.getLogger(__name__)


class MediaProcessingError(Exception):
    """Raised when video download or media extraction fails."""
    pass


class MediaService:
    def __init__(self, temp_dir: str = settings.STORAGE_TEMP_DIR):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def download_video(self, url: str) -> str:
        """Download social media video (Instagram, TikTok, X) using yt-dlp.
        
        Returns the absolute path to the downloaded MP4 file.
        """
        import yt_dlp

        session_id = uuid.uuid4().hex[:10]
        output_template = str(self.temp_dir / f"video_{session_id}.%(ext)s")

        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": output_template,
            "quiet": True,
            "no_warnings": True,
            "merge_output_format": "mp4",
        }

        try:
            logger.info("Starting yt-dlp download for URL: %s", url)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                # If merged, filename extension is mp4
                base, _ = os.path.splitext(filename)
                target_mp4 = f"{base}.mp4"
                if os.path.exists(target_mp4):
                    return target_mp4
                if os.path.exists(filename):
                    return filename
                raise FileNotFoundError(f"Downloaded file not found for: {filename}")
        except Exception as exc:
            logger.error("Failed to download video from %s: %s", url, exc)
            raise MediaProcessingError(f"yt-dlp download error: {exc}") from exc

    def extract_audio(self, video_path: str) -> str:
        """Extract audio track as MP3 from MP4 video using ffmpeg."""
        import ffmpeg

        video_file = Path(video_path)
        audio_path = video_file.with_suffix(".mp3")

        try:
            logger.info("Extracting audio from %s to %s", video_path, audio_path)
            (
                ffmpeg.input(video_path)
                .output(str(audio_path), vn=None, acodec="libmp3lame", qscale=2)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            return str(audio_path)
        except Exception as exc:
            logger.error("Audio extraction failed for %s: %s", video_path, exc)
            raise MediaProcessingError(f"Audio extraction error: {exc}") from exc

    def extract_keyframes(self, video_path: str, num_frames: int = 3) -> List[str]:
        """Extract representative keyframe images (.jpg) from video using ffmpeg."""
        import ffmpeg

        video_file = Path(video_path)
        session_id = video_file.stem
        frames: List[str] = []

        try:
            # Probe video duration to space frames evenly
            probe = ffmpeg.probe(video_path)
            duration = float(probe["format"]["duration"])
            intervals = [duration * (i + 1) / (num_frames + 1) for i in range(num_frames)]

            for idx, timestamp in enumerate(intervals):
                frame_path = self.temp_dir / f"{session_id}_frame_{idx + 1}.jpg"
                (
                    ffmpeg.input(video_path, ss=timestamp)
                    .output(str(frame_path), vframes=1)
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )
                frames.append(str(frame_path))

            logger.info("Extracted %d keyframes from %s", len(frames), video_path)
            return frames
        except Exception as exc:
            logger.warning("Dynamic keyframe extraction failed, falling back to fps filter: %s", exc)
            try:
                frame_pattern = str(self.temp_dir / f"{session_id}_frame_%02d.jpg")
                (
                    ffmpeg.input(video_path)
                    .filter("fps", fps=0.5)
                    .output(frame_pattern, vframes=num_frames)
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )
                # Collect generated frames
                generated = sorted(str(p) for p in self.temp_dir.glob(f"{session_id}_frame_*.jpg"))
                return generated[:num_frames]
            except Exception as inner_exc:
                logger.error("Fallback keyframe extraction failed: %s", inner_exc)
                raise MediaProcessingError(f"Keyframe extraction error: {inner_exc}") from inner_exc

    def cleanup_media(self, *file_paths: str) -> None:
        """Remove specified media files from storage to prevent disk bloat."""
        for path_str in file_paths:
            if not path_str:
                continue
            path = Path(path_str)
            try:
                if path.is_file():
                    path.unlink(missing_ok=True)
                elif path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
            except Exception as exc:
                logger.warning("Failed to clean up temporary path %s: %s", path_str, exc)


media_service = MediaService()
