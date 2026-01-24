# tests/scenarios/qlib/exhaustive_search/test_factor_library.py
import pytest

from rdagent.scenarios.qlib.exhaustive_search.layer1.factor_library import FactorLibrary


def test_factor_library_initialization():
    """Test that factor library can be initialized"""
    lib = FactorLibrary()
    assert len(lib.get_all_factors()) > 0


def test_get_alpha158_factors():
    """Test getting Alpha158 baseline factors"""
    lib = FactorLibrary()
    alpha158 = lib.get_alpha158_factors()

    # Should have 20 baseline factors
    assert len(alpha158) == 20

    # Check structure
    factor = alpha158[0]
    assert "name" in factor
    assert "formula" in factor


def test_get_custom_research_factors():
    """Test getting custom research factors"""
    lib = FactorLibrary()
    custom = lib.get_custom_research_factors()

    # Should include our best factors from previous experiments
    factor_names = [f["name"] for f in custom]

    assert "Price_Distance_Z_5D" in factor_names
    assert "VPT_5D" in factor_names


def test_get_all_factors():
    """Test getting all factors from all sources"""
    lib = FactorLibrary()
    all_factors = lib.get_all_factors()

    # Should have factors from multiple sources
    assert len(all_factors) >= 20  # At least Alpha158

    # Check for duplicates (should be none)
    names = [f["name"] for f in all_factors]
    assert len(names) == len(set(names))
