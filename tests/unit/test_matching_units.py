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


def test_bare_gallon_parses_for_milk():
    size = parse_size("2% milk gallon", category="milk")

    assert size.value == 128
    assert size.unit == "fl_oz"


def test_product_name_bare_gallon_parses_for_milk():
    size = parse_size("Great Value 2% Milk, Gallon", category="milk")

    assert size.value == 128
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


# --- metric units ---


def test_milliliter_parses_to_ml():
    size = parse_size("sparkling water 500 ml")

    assert size.value == 500
    assert size.unit == "ml"


def test_liter_converts_to_ml():
    size = parse_size("olive oil 1 liter")

    assert size.value == 1000
    assert size.unit == "ml"


# --- each unit ---


def test_each_parses_for_produce():
    size = parse_size("avocado 1 each", category="produce")

    assert size.value == 1
    assert size.unit == "each"


# --- sq_ft unit ---


def test_sq_ft_parses_for_paper_goods():
    size = parse_size("paper towels 6 rolls 150 sq ft", category="paper_goods")

    assert size.value == 150
    assert size.unit == "sq_ft"


# --- comma-separated multipack ---


def test_comma_multipack_walmart_format():
    size = parse_size("6 pk, 16.9 fl oz")

    assert size.value == 6 * 16.9
    assert size.unit == "fl_oz"


# --- unicode multiply ---


def test_multipack_unicode_multiply():
    size = parse_size("6 × 8 oz cups")

    assert size.value == 48
    assert size.unit == "oz"


# --- twin pack ---


def test_twin_pack_parses_total():
    size = parse_size("twin pack 64 fl oz")

    assert size.value == 128
    assert size.unit == "fl_oz"


def test_double_pack_parses_total():
    size = parse_size("double pack 16 oz")

    assert size.value == 32
    assert size.unit == "oz"


# --- total / net weight ---


def test_total_weight_overrides_per_unit():
    size = parse_size("6 pouches 8 oz each total weight 48 oz")

    assert size.value == 48
    assert size.unit == "oz"


def test_net_wt_parses():
    size = parse_size("net wt. 24 oz")

    assert size.value == 24
    assert size.unit == "oz"


# --- cross-unit compatibility ---


def test_fl_oz_and_ml_are_compatible():
    fl_oz = parse_size("33.8 fl oz")
    ml = parse_size("1000 ml")

    assert sizes_compatible(fl_oz, ml)


def test_meat_prefers_weight_over_count():
    size = parse_size("chicken breast 4 ct 2.5 lb", category="chicken")

    assert size.unit == "oz"
    assert size.value == 40
