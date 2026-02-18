from dataclasses import dataclass
from vmray_consts import INDEX_LOG_DELIMITER


@dataclass
class ScreenshotLogEntry:
    timestamp: int
    file_size: int
    md5: str
    sha1: str
    sha256: str
    filename: str

    @classmethod
    def parse(cls, line: str) -> "ScreenshotLogEntry":
        """Parse a log line and return a ScreenshotLogEntry instance."""
        parts = [part.strip() for part in line.split(INDEX_LOG_DELIMITER)]

        if len(parts) != 4:
            raise ValueError(
                f"Expected 4 parts separated by `{INDEX_LOG_DELIMITER}`, got {len(parts)}"
            )

        timestamp = int(parts[0])
        file_size = int(parts[1])
        filename = parts[3]

        # Parse the hash string
        hashes = {}
        for hash_pair in parts[2].split(","):
            key, value = hash_pair.split("=")
            hashes[key] = value

        return cls(
            timestamp=timestamp,
            file_size=file_size,
            md5=hashes["md5"],
            sha1=hashes["sha1"],
            sha256=hashes["sha256"],
            filename=filename,
        )
