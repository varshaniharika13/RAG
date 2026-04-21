from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True)
class ChunkConfig:
    size: int = 700
    overlap: int = 100
    separators: tuple[str, ...] = ("\n\n", "\n", ". ")


def fixed_chunk(text: str, size: int = 700, overlap: int = 100) -> list[str]:
    if size <= overlap:
        raise ValueError("Chunk size must be larger than overlap")
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start = max(0, end - overlap)
    return [chunk for chunk in chunks if chunk]


def heading_aware_chunk(text: str, max_chars: int = 1000) -> list[str]:
    heading_pattern = re.compile(r"^#{1,6}\s+.+$", re.MULTILINE)
    indices = [m.start() for m in heading_pattern.finditer(text)]
    if not indices:
        return fixed_chunk(text, size=max_chars, overlap=max_chars // 6)

    indices.append(len(text))
    chunks: list[str] = []
    for i in range(len(indices) - 1):
        section = text[indices[i] : indices[i + 1]].strip()
        if len(section) <= max_chars:
            chunks.append(section)
        else:
            chunks.extend(fixed_chunk(section, size=max_chars, overlap=max_chars // 8))
    return chunks


def recursive_chunk(text: str, config: ChunkConfig | None = None) -> list[str]:
    cfg = config or ChunkConfig()

    def _split(segment: str, level: int) -> list[str]:
        if len(segment) <= cfg.size:
            return [segment.strip()]
        if level >= len(cfg.separators):
            return fixed_chunk(segment, size=cfg.size, overlap=cfg.overlap)

        sep = cfg.separators[level]
        parts = [part.strip() for part in segment.split(sep) if part.strip()]
        if len(parts) <= 1:
            return _split(segment, level + 1)

        merged: list[str] = []
        current = ""
        for part in parts:
            candidate = f"{current}{sep}{part}" if current else part
            if len(candidate) <= cfg.size:
                current = candidate
            else:
                if current:
                    merged.append(current.strip())
                if len(part) > cfg.size:
                    merged.extend(_split(part, level + 1))
                    current = ""
                else:
                    current = part
        if current:
            merged.append(current.strip())
        return merged

    return [c for c in _split(text, 0) if c]
