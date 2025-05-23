"""Test i18n/es."""

# external
import pytest

# local
from validators import ValidationError, es_cif, es_doi, es_nie, es_nif


@pytest.mark.parametrize(
    ("value",),
    [
        ("B25162520",),
        ("U4839822F",),
        ("B96817697",),
        ("P7067074J",),
        ("Q7899705C",),
        ("C75098681",),
        ("G76061860",),
        ("C71345375",),
        ("G20558169",),
        ("U5021960I",),
    ],
)
def test_returns_true_on_valid_cif(value: str):
    """Test returns true on valid cif."""
    assert es_cif(value)


@pytest.mark.parametrize(
    ("value",),
    [
        ("12345",),
        ("ABCDEFGHI",),
        ("Z5021960I",),
    ],
)
def test_returns_false_on_invalid_cif(value: str):
    """Test returns false on invalid cif."""
    result = es_cif(value)
    assert isinstance(result, ValidationError)


@pytest.mark.parametrize(
    ("value",),
    [
        ("X0095892M",),
        ("X8868108K",),
        ("X2911154K",),
        ("Y2584969J",),
        ("X7536157T",),
        ("Y5840388N",),
        ("Z2915723H",),
        ("Y4002236C",),
        ("X7750702R",),
        ("Y0408759V",),
    ],
)
def test_returns_true_on_valid_nie(value: str):
    """Test returns true on valid nie."""
    assert es_nie(value)


@pytest.mark.parametrize(
    ("value",),
    [
        ("K0000023T",),
        ("L0000024R",),
        ("M0000025W",),
        ("00000026A",),
        ("00000027G",),
        ("00000028M",),
        ("00000029Y",),
        ("00000030F",),
        ("00000031P",),
        ("00000032D",),
        ("00000033X",),
        ("00000034B",),
        ("00000035N",),
        ("00000036J",),
        ("00000037Z",),
        ("00000038S",),
        ("00000039Q",),
        ("00000040V",),
        ("00000041H",),
        ("00000042L",),
        ("00000043C",),
        ("00000044K",),
        ("00000045E",),
    ],
)
def test_returns_true_on_valid_nif(value: str):
    """Test returns true on valid nif."""
    assert es_nif(value)


def test_returns_false_on_invalid_nif():
    """Test returns false on invalid nif."""
    result = es_nif("12345")
    assert isinstance(result, ValidationError)


@pytest.mark.parametrize(
    ("value",),
    [
        # CIFs
        ("B25162520",),
        ("U4839822F",),
        ("B96817697",),
        # NIEs
        ("X0000000T",),
        ("X0095892M",),
        ("X8868108K",),
        ("X2911154K",),
        # NIFs
        ("00000001R",),
        ("00000000T",),
        ("26643189N",),
        ("07060225F",),
        ("49166693F",),
    ],
)
def test_returns_true_on_valid_doi(value: str):
    """Test returns true on valid doi."""
    assert es_doi(value)
