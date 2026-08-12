"""Provides support for a local cache for remote content."""

##############################################################################
# Python imports.
from datetime import datetime
from json import JSONDecodeError, dumps, loads
from pathlib import Path
from shutil import rmtree

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
        return cache_path.with_suffix(".meta"), cache_path.with_suffix(".content")

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

    def clear(self) -> None:
        """Clear the cache."""
        rmtree(self.base_path, ignore_errors=True)


### cache.py ends here
