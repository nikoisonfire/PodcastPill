import sys
import time

from dotenv import dotenv_values

from pull_service.api_controller import calculate_auth_headers, pull_frequency_data
from pull_service.utils import load_file

config = dotenv_values("../.env")


def main():
    # Re
    headers = calculate_auth_headers(config)
    data = load_file("podcast_data.json")

    t1 = time.perf_counter()

    pod_data = pull_frequency_data(data, headers, 0, 20)

    t2 = time.perf_counter()
    print(f"Finished in {t2 - t1} seconds")

    # write_to_db(pod_data, "podpill.db")
    sys.exit(0)


if __name__ == "__main__":
    main()
