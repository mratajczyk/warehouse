from unittest.mock import Mock, call
from unittest.mock import mock_open as mock_file_open_helper

import pytest

from api.config.read import prepare, read_from_file


def test_read_from_file(mocker):
    """
    GIVEN read_config function
    WHEN reading configuration from a file in given path
    THEN check if file was opened properly and yaml content was parsed
    """
    mocked_open = mock_file_open_helper(read_data="test_key: test_value")
    mocker.patch("builtins.open", mocked_open)

    result = read_from_file("foo", path="mocked/path")

    assert result == dict(test_key="test_value")
    assert mocked_open.call_args == call("mocked/path/foo")


@pytest.mark.parametrize(
    "base,overwrite,env,expected",
    [
        (
            dict(baseConfigItemOne="foo", baseConfigItemTwo="foo", password="empty"),
            dict(baseConfigItemOne="bar", overwriteConfigItemOne="bar"),
            dict(envVariable="fooBar", password="secret"),
            dict(
                baseConfigItemOne="bar",
                overwriteConfigItemOne="bar",
                baseConfigItemTwo="foo",
                envVariable="fooBar",
                password="secret",
            ),
        ),
        (
            dict(baseConfigItemOne="foo", baseConfigItemTwo="foo"),
            dict(),
            dict(),
            dict(
                baseConfigItemOne="foo",
                baseConfigItemTwo="foo",
            ),
        ),
        (
            dict(),
            dict(overwriteConfigItemOne="bar"),
            dict(),
            dict(overwriteConfigItemOne="bar"),
        ),
        (
            dict(),
            dict(),
            dict(),
            dict(),
        ),
    ],
)
def test_prepare(mocker, base, overwrite, env, expected):
    """
    GIVEN prepare function
    WHEN calling function
    THEN check if configs coming from base/overwrite file are merged properly
    """
    mock_read_config = Mock(side_effect=[base, overwrite])
    mocker.patch("api.config.read.read_from_file", mock_read_config)
    mocker.patch("api.config.read.read_from_env", Mock(return_value=env))
    assert prepare() == expected
