"""Pydantic models for DoomsdayWatch config + runtime state.

These enforce the contract between the cron writer and the pipeline. If the
cron writes malformed state, validation fails loudly at pipeline startup
instead of producing a silently broken dashboard.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ── Config (tracker_config.json) ──────────────────────────────────────────────


class SignalConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    weight: float


class TrackerConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    base_rate: float
    description: str = ""
    signals: Dict[str, SignalConfig] = Field(default_factory=dict)


class CouplingBlock(BaseModel):
    model_config = ConfigDict(extra="allow")
    affects: Dict[str, float] = Field(default_factory=dict)


class ScoringZones(BaseModel):
    model_config = ConfigDict(extra="allow")
    deterrent: List[float] = Field(default_factory=lambda: [0, 15])
    elevated: List[float] = Field(default_factory=lambda: [15, 30])
    critical: List[float] = Field(default_factory=lambda: [30, 60])
    imminent: List[float] = Field(default_factory=lambda: [60, 100])


class Scoring(BaseModel):
    model_config = ConfigDict(extra="allow")
    zones: ScoringZones = Field(default_factory=ScoringZones)


class TrackerConfigRoot(BaseModel):
    """Schema for tracker_config.json."""

    model_config = ConfigDict(extra="allow")
    zones: List[str] = Field(default_factory=list)
    signal_weights: Dict[str, float] = Field(default_factory=dict)
    trackers: Dict[str, TrackerConfig] = Field(default_factory=dict)
    coupling: Dict[str, CouplingBlock] = Field(default_factory=dict)
    scoring: Scoring = Field(default_factory=Scoring)
    global_weights: Dict[str, float] = Field(default_factory=dict)
    dashboard_path: str = "dashboard.html"


# ── Runtime state (current_state.json) ────────────────────────────────────────


class ZoneSignals(BaseModel):
    """Qualitative per-dimension signal severities written by the cron."""

    model_config = ConfigDict(extra="allow")


class ZoneBlock(BaseModel):
    """Qualitative tracker entry in state.zones{}."""

    model_config = ConfigDict(extra="allow")
    name: str
    base_prob: float
    current_prob: float
    trend: str
    signals: Dict[str, str] = Field(default_factory=dict)
    notes: str = ""
    zone: str = "deterrent"


class TrackerBlock(BaseModel):
    """Synthesized tracker record — pipeline maintains this."""

    model_config = ConfigDict(extra="allow")
    name: str
    current_probability: float
    trend: str
    active_signals: List[str] = Field(default_factory=list)
    zone: str = "deterrent"
    current_probability_with_coupling: Optional[float] = None
    coupling_boost: float = 0.0


class CurrentState(BaseModel):
    """Top-level schema for current_state.json."""

    model_config = ConfigDict(extra="allow")
    timestamp: Optional[str] = None
    last_updated: str
    zones: Dict[str, ZoneBlock] = Field(default_factory=dict)
    trackers: Dict[str, TrackerBlock] = Field(default_factory=dict)
    doomsday_clock_minutes: Optional[float] = None
    global_war_probability: Optional[float] = None
    global_zone: Optional[str] = None
    predictions: List[Dict[str, Any]] = Field(default_factory=list)
    eval_stats: Optional[Dict[str, Any]] = None

    @field_validator("doomsday_clock_minutes")
    @classmethod
    def _clamp_doomsday(cls, v):
        # Published value has been under 2 min for years; anything huge is a bug.
        if v is None:
            return v
        if v < 0:
            raise ValueError(f"doomsday_clock_minutes must be >= 0, got {v}")
        return v


# ── Public helpers ────────────────────────────────────────────────────────────


def validate_config(raw: dict) -> TrackerConfigRoot:
    return TrackerConfigRoot.model_validate(raw)


def validate_state(raw: dict) -> CurrentState:
    return CurrentState.model_validate(raw)
