import sys
import loggers

from dotenv import dotenv_values

from api_pull_service.api_controller import calculate_auth_headers, pull_frequency_data
from api_pull_service.db_controller import write_to_db
from api_pull_service.utils import load_file

config = dotenv_values("../.env")


def main():
    # Re
    headers = calculate_auth_headers(config)
    data = load_file("podcast_data.json")

    pod_data = pull_frequency_data(data, headers, 5)

    write_to_db(pod_data, "podpill.db")

    sys.exit(0)


if __name__ == "__main__":
    main()
