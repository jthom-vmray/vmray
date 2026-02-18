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


TEST_CASES = [
    {
        "timestamp": 0,
        "file_size": 83811,
        "md5": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "sha1": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    },
    {
        "timestamp": 39235,
        "file_size": 66172,
        "md5": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "sha1": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    },
    {
        "timestamp": 41186,
        "file_size": 49366,
        "md5": "cccccccccccccccccccccccccccccccc",
        "sha1": "cccccccccccccccccccccccccccccccccccccccc",
        "sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
    },
]


def make_line(tc: dict) -> str:
    return f"{tc['timestamp']} | {tc['file_size']} | md5={tc['md5']},sha1={tc['sha1']},sha256={tc['sha256']} | {tc['sha1']}.jpg"


def make_entry(tc: dict) -> ScreenshotLogEntry:
    return ScreenshotLogEntry(
        timestamp=tc["timestamp"],
        file_size=tc["file_size"],
        md5=tc["md5"],
        sha1=tc["sha1"],
        sha256=tc["sha256"],
        filename=f"{tc['sha1']}.jpg",
    )


@pytest.mark.parametrize("tc", TEST_CASES)
def test_parse_valid_line(tc):
    assert ScreenshotLogEntry.parse(make_line(tc)) == make_entry(tc)


@pytest.mark.parametrize("tc", TEST_CASES)
def test_parse_timestamp(tc):
    assert ScreenshotLogEntry.parse(make_line(tc)).timestamp == tc["timestamp"]


@pytest.mark.parametrize("tc", TEST_CASES)
def test_parse_file_size(tc):
    assert ScreenshotLogEntry.parse(make_line(tc)).file_size == tc["file_size"]


@pytest.mark.parametrize("tc", TEST_CASES)
def test_parse_hashes(tc):
    result = ScreenshotLogEntry.parse(make_line(tc))
    assert result.md5 == tc["md5"]
    assert result.sha1 == tc["sha1"]
    assert result.sha256 == tc["sha256"]


@pytest.mark.parametrize("tc", TEST_CASES)
def test_parse_filename(tc):
    assert ScreenshotLogEntry.parse(make_line(tc)).filename == f"{tc['sha1']}.jpg"


def test_parse_invalid_too_few_parts():
    with pytest.raises(ValueError, match="Expected 4 parts"):
        ScreenshotLogEntry.parse("0 | 83811 | md5=abc")


def test_parse_invalid_too_many_parts():
    with pytest.raises(ValueError, match="Expected 4 parts"):
        ScreenshotLogEntry.parse("0 | 83811 | md5=abc | file.jpg | extra")


def test_parse_invalid_timestamp():
    with pytest.raises(ValueError):
        ScreenshotLogEntry.parse("not_a_number | 83811 | md5=abc,sha1=def,sha256=ghi | file.jpg")


def test_parse_invalid_file_size():
    with pytest.raises(ValueError):
        ScreenshotLogEntry.parse("0 | not_a_number | md5=abc,sha1=def,sha256=ghi | file.jpg")
