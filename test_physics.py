from physics import speed, position, speed_in_units, convert_distance_to_m, convert_time_to_s

def test_basic_speed():
    assert speed(100, 10) == 10

def test_position():
    assert position(100, 10, 4) == 40
    assert position(100, 10, 20) == 100

def test_units():
    assert convert_distance_to_m(1, "km") == 1000
    assert convert_time_to_s(1, "min") == 60
    assert speed_in_units(10, "km", "h") == 36

if __name__ == "__main__":
    test_basic_speed()
    test_position()
    test_units()
    print("All physics tests passed.")
