"""Packs units into chunks: never across sections, cut only between units, with a small overlap."""
import hashlib
from dataclasses import dataclass

from app.ingest.parse import ParsedArticle, Unit


@dataclass
class Chunk:
    index: int
    section_path: str
    units: list[Unit]

    @property
    def text(self) -> str:
        return " ".join(u.text for u in self.units)

    @property
    def start(self) -> int:
        return self.units[0].start

    @property
    def end(self) -> int:
        return self.units[-1].end

    def embed_text(self, title: str) -> str:
        return f"{title} > {self.section_path}\n{self.text}"

    def content_hash(self, title: str) -> str:
        return hashlib.sha256(self.embed_text(title).encode()).hexdigest()


def _words(unit: Unit) -> int:
    return len(unit.text.split())


def chunk_article(parsed: ParsedArticle, target_words: int, overlap_words: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    for section in parsed.sections:
        path = " > ".join(section.path[1:]) or section.path[0]
        units = section.units
        i = 0
        while i < len(units):
            batch: list[Unit] = []
            words = 0
            j = i
            while j < len(units) and (not batch or words + _words(units[j]) <= target_words):
                batch.append(units[j])
                words += _words(units[j])
                j += 1
            chunks.append(Chunk(index=len(chunks), section_path=path, units=batch))
            if j >= len(units):
                break
            # Step back over trailing units for overlap, but always make progress.
            back, k = 0, j
            while k - 1 > i and back + _words(units[k - 1]) <= overlap_words:
                k -= 1
                back += _words(units[k])
            i = max(k, i + 1)
    return chunks
