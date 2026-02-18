# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
            raise ValueError(f"Expected 4 parts separated by `{INDEX_LOG_DELIMITER}`, got {len(parts)}")

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
