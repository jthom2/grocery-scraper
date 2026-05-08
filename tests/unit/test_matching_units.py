from app.matching.units import parse_size, sizes_compatible


def test_gallon_equals_fluid_ounces():
    gallon = parse_size("1 gal")
    ounces = parse_size("128 fl oz")

    assert gallon.unit == "fl_oz"
    assert ounces.unit == "fl_oz"
    assert sizes_compatible(gallon, ounces)


def test_pound_equals_ounces():
    pound = parse_size("1 lb")
    ounces = parse_size("16 oz")

    assert pound.unit == "oz"
    assert ounces.unit == "oz"
    assert sizes_compatible(pound, ounces)


def test_dozen_parses_to_count():
    size = parse_size("large eggs dozen")

    assert size.value == 12
    assert size.unit == "ct"


def test_half_gallon_parses_to_fluid_ounces():
    size = parse_size("half gallon 2% milk")

    assert size.value == 64
    assert size.unit == "fl_oz"


def test_numeric_half_gallon_parses_to_fluid_ounces():
    size = parse_size("1/2 gal 2% milk")

    assert size.value == 64
    assert size.unit == "fl_oz"


def test_mixed_fraction_parses_to_normalized_weight():
    size = parse_size("1 1/2 lb loaf")

    assert size.value == 24
    assert size.unit == "oz"


def test_multipack_x_form_parses_total_measured_size():
    size = parse_size("6 x 8 oz cups")

    assert size.value == 48
    assert size.unit == "oz"


def test_multipack_dash_form_parses_total_measured_size():
    size = parse_size("6-pack 8 oz bottles")

    assert size.value == 48
    assert size.unit == "oz"


def test_non_egg_product_prefers_weight_over_pack_count():
    size = parse_size("butter 4 sticks 16 oz", category="butter")

    assert size.value == 16
    assert size.unit == "oz"
