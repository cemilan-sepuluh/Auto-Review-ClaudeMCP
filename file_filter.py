"""File filtering rules — which extensions to include/skip in PR reviews."""

from pathlib import Path

ALLOWED_EXTENSIONS = {
    ".cs", ".json", ".xml", ".yaml", ".yml",
    ".asmdef", ".asmref", ".md", ".txt",
    ".gradle", ".java", ".kt", ".sh", ".py",
}

BLOCKED_EXTENSIONS = {
    ".meta", ".prefab", ".unity", ".asset", ".mat",
    ".fbx", ".obj", ".blend", ".png", ".jpg", ".jpeg",
    ".tga", ".psd", ".mp3", ".wav", ".ogg", ".mp4",
    ".shader", ".dll", ".so", ".ttf", ".otf",
    ".controller", ".overrideController", ".anim",
    ".playable", ".mixer", ".lighting", ".giparams",
}


def should_include(filename: str) -> bool:
    """Return True if the file should be included in a PR review."""
    ext = Path(filename).suffix.lower()
    if ext in BLOCKED_EXTENSIONS:
        return False
    return ext in ALLOWED_EXTENSIONS
