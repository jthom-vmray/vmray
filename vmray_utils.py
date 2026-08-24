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
    filename: str

    @classmethod
    def parse(cls, line: str) -> "ScreenshotLogEntry":
        """Parse a log line and return a ScreenshotLogEntry instance."""
        parts = [part.strip() for part in line.split(INDEX_LOG_DELIMITER)]

        if len(parts) < 4:
            raise ValueError(f"Expected at least 4 parts separated by `{INDEX_LOG_DELIMITER}`, got {len(parts)}")

        return cls(filename=parts[-1])
