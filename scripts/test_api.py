import requests

BASE_URL = "http://127.0.0.1:8000"


def print_response(label: str, response: requests.Response) -> None:
    print(f"\n--- {label} ---")
    print(f"Status: {response.status_code}")
    try:
        print(response.json())
    except Exception:
        print(response.text)


def main() -> None:
    r = requests.get(f"{BASE_URL}/health")
    print_response("GET /health", r)

    r = requests.get(f"{BASE_URL}/state")
    print_response("GET /state (initial)", r)

    r = requests.post(
        f"{BASE_URL}/set_signal_attenuation",
        json={"value_db": 12.63},  # rounds to 12.75
    )
    print_response("POST /set_signal_attenuation", r)

    r = requests.post(
        f"{BASE_URL}/set_noise_attenuation",
        json={"value_db": 80.1},  # rejected (>80)
    )
    print_response("POST /set_noise_attenuation (invalid > 80 dB)", r)

    r = requests.post(
        f"{BASE_URL}/set_noise_attenuation",
        json={"value_db": 18.12},  # rounds to 18.0
    )
    print_response("POST /set_noise_attenuation", r)

    r = requests.post(f"{BASE_URL}/enable_noise")
    print_response("POST /enable_noise", r)

    r = requests.post(f"{BASE_URL}/disable_noise")
    print_response("POST /disable_noise", r)

    r = requests.post(
        f"{BASE_URL}/set_doppler",
        json={"shift_hz": 35000},
    )
    print_response("POST /set_doppler", r)

    r = requests.post(
        f"{BASE_URL}/select_measurement_point",
        json={"point": "rf2"},
    )
    print_response("POST /select_measurement_point", r)

    r = requests.get(f"{BASE_URL}/read_power")
    print_response("GET /read_power", r)

    r = requests.get(f"{BASE_URL}/state")
    print_response("GET /state (final)", r)


if __name__ == "__main__":
    main()
