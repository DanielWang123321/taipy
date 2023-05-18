# Copyright 2023 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import re
from argparse import Namespace
from unittest.mock import patch

import pytest

from src.taipy._entrypoint import _entrypoint


def preprocess_stdout(stdout):
    stdout = stdout.replace("\n", " ").replace("\t", " ")
    return re.sub(" +", " ", stdout)


def test_taipy_help(capsys):
    expected_help = """{manage-versions,create,help} ...

positional arguments:
  {manage-versions,create,help}
    manage-versions         Taipy version control system.
    create          Create a new Taipy application.
    help                Show the Taipy help message.
"""

    with patch("sys.argv", ["prog"]):
        _entrypoint()
        out, _ = capsys.readouterr()
        assert preprocess_stdout(expected_help) in preprocess_stdout(out)

    with patch("sys.argv", ["prog", "help"]):
        with pytest.raises(SystemExit):
            _entrypoint()
        out, _ = capsys.readouterr()
        assert preprocess_stdout(expected_help) in preprocess_stdout(out)

    with patch("sys.argv", ["prog", "--help"]):
        with pytest.raises(SystemExit):
            _entrypoint()
        out, _ = capsys.readouterr()
        assert preprocess_stdout(expected_help) in preprocess_stdout(out)


def test_help_non_existed_command(caplog):
    # with patch("sys.argv", ["prog", "help", "non_existed_command"]):
    with patch("taipy._cli._base_cli._CLI._parse", return_value=Namespace(which="help", command="non_existed_command")):
        with pytest.raises(SystemExit):
            _entrypoint()
        assert "non_existed_command is not a valid command." in caplog.text


def test_taipy_create_help(capsys):
    expected_help = "create [-h] [--template"

    with patch("sys.argv", ["prog", "create", "--help"]):
        with pytest.raises(SystemExit):
            _entrypoint()
        out, _ = capsys.readouterr()
        assert preprocess_stdout(expected_help) in preprocess_stdout(out)

    # with patch("sys.argv", ["prog", "help", "create"]):
    with patch("taipy._cli._base_cli._CLI._parse", return_value=Namespace(which="help", command="create")):
        with pytest.raises(SystemExit):
            _entrypoint()
        out, _ = capsys.readouterr()
        assert preprocess_stdout(expected_help) in preprocess_stdout(out)