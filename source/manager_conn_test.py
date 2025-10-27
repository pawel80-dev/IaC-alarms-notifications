from manager_api import manager_connectivity_test
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="Manager API URL")
# parser.add_argument("code_url", type=str, help="Twilio function code upload API URL")
# parser.add_argument("account_sid", type=str, help="Twilio account SID")
# parser.add_argument("auth_token", type=str, help="Twilio authentication token")
# parser.add_argument("service_sid", type=str, help="Twilio service SID")
# parser.add_argument("func_sid", type=str, help="Twilio function SID")
# parser.add_argument("env_sid", type=str, help="Twilio environment SID")
# parser.add_argument("code_location", type=str, help="Twilio Node.JS code path")
args = parser.parse_args()


def main():
    manager_connectivity_test(args.url)


if __name__ == "__main__":
    main()