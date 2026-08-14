"""Provides support for a local cache for remote content."""

##############################################################################
# Python imports.
from datetime import datetime
from json import JSONDecodeError, dumps, loads
from pathlib import Path
from shutil import rmtree
from typing import Callable, Final

##############################################################################
# BagOfStuff imports.
from bagofstuff.cache import CacheManager

##############################################################################
# Local imports.
from .data import load_configuration
from .data.locations import cache_dir
from .document import Document
from .preflight import make_location
from .types import RogalloLocation


##############################################################################
class ContentCache(CacheManager):
    """A cache manager for remote content."""

    _META: Final[str] = ".meta"
    """The suffix for the metadata files in the cache."""
    _CONTENT: Final[str] = ".content"
    """The suffix for the content files in the cache."""

    def __init__(self) -> None:
        """Initialise the content cache."""
        super().__init__(cache_dir())
        self._disabled = not load_configuration().with_cache
        """Whether the cache is disabled."""
        self._ttl = load_configuration().cache_ttl
        """The time-to-live for cached content, in seconds."""

    def _cache_files(self, uri: RogalloLocation) -> tuple[Path, Path]:
        """Get the paths to the cache files.

        Args:
            uri: The URI to get the cache files for.

        Returns:
            A tuple containing the paths to the cache files.
        """
        cache_path = self.get(uri=uri)
        return cache_path.with_suffix(self._META), cache_path.with_suffix(self._CONTENT)

    def get_document(self, uri: RogalloLocation) -> Document | None:
        """Get a cached copy of a document for a given URI.

        Args:
            uri: The URI to get the cached copy for.

        Returns:
            The cached document, or `None` if it is not cached.
        """

        if self._disabled:
            return None

        meta_data_file, content_file = self._cache_files(uri)

        # Load the metadata.
        try:
            meta_data = loads(meta_data_file.read_text(encoding="utf-8"))
        except (OSError, JSONDecodeError):
            return None

        # In the unlikely event we can't work out when the document was
        # cached, treat it as not cached.
        if (cached_at := meta_data.get("cached_at")) is None:
            return None

        # See if the cached document has expired.
        if (
            datetime.now() - datetime.fromisoformat(cached_at)
        ).total_seconds() > self._ttl:
            return None

        # Load the content and return the document.
        try:
            return Document(
                location=uri,
                original_location=make_location(
                    meta_data.get("original_location", uri)
                ),
                content=content_file.read_text(encoding="utf-8"),
                mime_type=meta_data.get("mime_type"),
                verification_method=meta_data.get("verification_method"),
                from_cache=True,
            )
        except OSError:
            return None

    def add_document(self, document: Document) -> Document:
        """Add a document to the cache.

        Args:
            document: The document to cache.

        Returns:
            The document that was cached.
        """

        # Just return the document if the cache is disabled or the document
        # should avoid being cached.
        if self._disabled or document.avoid_cache or document.location is None:
            return document

        meta_data_file, content_file = self._cache_files(document.location)

        try:
            content_file.write_text(document.content, encoding="utf-8")
            meta_data_file.write_text(
                dumps(
                    {
                        "location": str(document.location),
                        "original_location": str(document.original_location),
                        "mime_type": document.mime_type,
                        "verification_method": document.verification_method,
                        "cached_at": datetime.now().isoformat(),
                    },
                    indent=4,
                ),
                encoding="utf-8",
            )
        except OSError:
            pass
        return document

    @classmethod
    def _reap(cls, meta_file: Path) -> None:
        """Reap a cache entry.

        Args:
            meta_file: The path to the metadata file for the cache entry.
        """
        try:
            meta_file.unlink()
            if (content_file := meta_file.with_suffix(cls._CONTENT)).exists():
                content_file.unlink()
        except OSError:
            pass

    def expire(self, cancelled: Callable[[], bool]) -> None:
        """Expire the cache."""
        if self._disabled or cancelled():
            return

        # Clean out any old files.
        for meta_file in self.base_path.glob(f"**/*{self._META}"):
            if cancelled():
                return
            if meta_file.is_file():
                # Try and load up the metadata.
                try:
                    meta_data = loads(meta_file.read_text(encoding="utf-8"))
                except JSONDecodeError:
                    # If we can't decode the metadata, it's probably
                    # corrupted. Reap it.
                    self._reap(meta_file)
                    continue
                except OSError:
                    continue

                # Get when the document was cached. If we can't work it out,
                # it's probably corrupted. Reap it.
                if (cached_at := meta_data.get("cached_at")) is None:
                    self._reap(meta_file)
                    continue

                # See if the cached document has expired. If it has, reap it.
                if (
                    datetime.now() - datetime.fromisoformat(cached_at)
                ).total_seconds() > self._ttl:
                    self._reap(meta_file)

        # Don't even try and clean out empty directories if the worker has
        # been cancelled.
        if cancelled():
            return

        # Clean out any empty directories.
        for directory in self.base_path.iterdir():
            if cancelled():
                return
            if directory.is_dir() and not any(directory.iterdir()):
                try:
                    directory.rmdir()
                except OSError:
                    pass

    def clear(self) -> None:
        """Clear the cache."""
        rmtree(self.base_path, ignore_errors=True)


### cache.py ends here
