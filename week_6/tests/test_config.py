"""Tests for configuration management."""

from week_6.api.config import get_config, DevConfig, TestConfig


def test_get_config_default() -> None:
    """Default config returns DevConfig."""
    cfg = get_config()
    assert cfg is DevConfig


def test_get_config_testing() -> None:
    """Explicit 'testing' config returns TestConfig."""
    cfg = get_config("testing")
    assert cfg is TestConfig


def test_get_config_invalid_returns_default() -> None:
    """Invalid config name falls back to default (DevConfig)."""
    cfg = get_config("invalid")
    assert cfg is DevConfig
