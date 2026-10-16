# coding=utf-8
# Copyright 2026 XRTM Team. All rights reserved.
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

r"""Normative markdown examples must be syntactically valid.

Governance is the schema authority; the copy-paste examples in ``schemas/``
used to rot unchecked (CI only validated ``*.json`` files).
"""

import ast
import json
import re
from pathlib import Path

import pytest

BLOCK_RE = re.compile(r"```(json|python)\n(.*?)```", re.DOTALL)
SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"


def _blocks():
    for path in sorted(SCHEMA_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for match in BLOCK_RE.finditer(text):
            yield path, match.group(1), match.group(2)


def test_doc_examples_are_valid_json_or_python():
    checked = 0
    for path, kind, body in _blocks():
        checked += 1
        if kind == "json":
            json.loads(body)
        else:
            ast.parse(body, filename=str(path))
    assert checked > 0


def test_schema_json_files_are_valid():
    files = sorted(SCHEMA_DIR.glob("*.json"))
    if not files:
        pytest.skip("no schema JSON files")
    for path in files:
        json.loads(path.read_text(encoding="utf-8"))
