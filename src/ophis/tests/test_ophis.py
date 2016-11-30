import pytest
import ophis


def test_project_defines_author_and_version():
    assert hasattr(ophis, '__author__')
    assert hasattr(ophis, '__version__')
