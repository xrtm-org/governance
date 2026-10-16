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

r"""Runtime conformance with the compatibility policy.

Alias round-trips and v1.2 telemetry fields, exercised against the released
runtime packages. CI installs ``xrtm-data``, ``xrtm-eval``, ``xrtm-forecast``
and ``xrtm-train`` from PyPI; the tests skip individually when a package is
unavailable locally.
"""

import pytest

COMMON = {"reasoning_trace": {"narrative": "n"}, "metadata": {"source_version": "test"}}


def test_forecast_output_legacy_aliases_round_trip():
    pytest.importorskip("xrtm.data")
    from xrtm.data.core.schemas.forecast import ForecastOutput

    output = ForecastOutput.model_validate(
        {"question_id": "q1", "confidence": 0.7, "structural_trace": ["a"], **COMMON}
    )

    assert output.forecast_request_id == "q1"
    assert output.probability == pytest.approx(0.7)
    assert output.execution_trace == ["a"]


def test_forecast_output_carries_v12_telemetry():
    pytest.importorskip("xrtm.data")
    from xrtm.data.core.schemas.forecast import ForecastOutput

    payload = ForecastOutput.model_validate(
        {"forecast_request_id": "q1", "probability": 0.7, **COMMON}
    ).model_dump(mode="json")

    for field in ("parse_status", "usage", "provenance"):
        assert field in payload


def test_resolution_legacy_alias_round_trips():
    pytest.importorskip("xrtm.eval")
    from datetime import datetime, timezone

    from xrtm.eval.core.schemas import ForecastResolution

    resolution = ForecastResolution.model_validate(
        {"question_id": "q1", "outcome": "yes", "resolved_at": datetime(2026, 1, 1, tzinfo=timezone.utc)}
    )

    assert resolution.forecast_request_id == "q1"


def test_benchmark_reporting_lane_alias_round_trips():
    pytest.importorskip("xrtm.train")
    from xrtm.train.simulation.benchmark_artifacts import ExternalBenchmarkSourceSpec

    spec = ExternalBenchmarkSourceSpec.model_validate(
        {
            "source_id": "src-1",
            "display_name": "Example",
            "source_name": "example",
            "system_id": "sys-1",
            "benchmark_id": "bench-1",
            "benchmark_name": "Example benchmark",
            "primary_score": 0.1,
            "primary_score_name": "brier",
            "reporting_lane": "public-leaderboard",
        }
    )

    assert spec.evaluation_path == "public-leaderboard"
    assert spec.reporting_lane == "public-leaderboard"
