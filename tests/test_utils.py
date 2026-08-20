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
import pytest

from vmray_utils import ScreenshotLogEntry


FILENAMES = ["aaaa.jpg", "bbbb.jpg", "cccc.jpg"]


def make_line(filename: str) -> str:
    return f"0 | 83811 | md5=aaaa,sha1=bbbb,sha256=cccc | {filename}"


@pytest.mark.parametrize("filename", FILENAMES)
def test_parse_valid_line(filename):
    assert ScreenshotLogEntry.parse(make_line(filename)) == ScreenshotLogEntry(filename=filename)


@pytest.mark.parametrize("filename", FILENAMES)
def test_parse_filename(filename):
    assert ScreenshotLogEntry.parse(make_line(filename)).filename == filename


def test_parse_tolerates_malformed_metadata():
    # timestamp, file_size, and hashes are all garbage, but the filename column is usable
    result = ScreenshotLogEntry.parse("not_a_number | not_a_number | md5=abc | file.jpg")
    assert result.filename == "file.jpg"


def test_parse_invalid_too_few_parts():
    with pytest.raises(ValueError, match="Expected at least 4 parts"):
        ScreenshotLogEntry.parse("0 | 83811 | md5=abc")


def test_parse_extra_parts_uses_last_as_filename():
    # more than 4 parts is tolerated; the last column is always taken as the filename
    result = ScreenshotLogEntry.parse("0 | 83811 | md5=abc | file.jpg | extra")
    assert result.filename == "extra"
