import pytest

from vmray_utils import ScreenshotLogEntry

TEST_CASES = [
    {
        "timestamp": 0,
        "file_size": 83811,
        "md5": "795acf142c6c5cd691591ae5ec1ee8eb",
        "sha1": "3ec5d670fe474878926e1d3fd3a0116454428df1",
        "sha256": "cfd0258707fbcdb838f53031a4cb6cd33981bcf83ff9346814240ab195193487",
    },
    {
        "timestamp": 39235,
        "file_size": 66172,
        "md5": "2b70f8e09150e2bec6bf403014fcbacc",
        "sha1": "7f951a15e976b2c38df47eb307a43344e3d30c96",
        "sha256": "75d4de94fafff2eabc93a0e061a90775e3300a05e00677d71a78f5f71bfb61c3",
    },
    {
        "timestamp": 41186,
        "file_size": 49366,
        "md5": "f2579bcece68f228bffa410c1de48160",
        "sha1": "b04da642fae7b5b37395b21d1eb01a9c5d1b84c3",
        "sha256": "85350234c3948b388317114bffb158bd2c68a2d1839730e0d6b00053f6bb2af1",
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
