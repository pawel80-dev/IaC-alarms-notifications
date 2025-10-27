from manager_api import (manager_connectivity_test, manager_jsession_id, manager_token, manager_logout,
                        alarm_notification)
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="Manager API URL")
parser.add_argument("username", type=str, help="Manager API username")
parser.add_argument("password", type=str, help="Manager API password")
# parser.add_argument("service_sid", type=str, help="Twilio service SID")
# parser.add_argument("func_sid", type=str, help="Twilio function SID")
# parser.add_argument("env_sid", type=str, help="Twilio environment SID")
# parser.add_argument("code_location", type=str, help="Twilio Node.JS code path")
args = parser.parse_args()


def main():
    # manager_connectivity_test(args.url)
    session_id = manager_jsession_id(args.url, args.username, args.password)
    token = manager_token(args.url, session_id)
    # alarm_notification(args.url, session_id, token)
    manager_logout(args.url, session_id)


if __name__ == "__main__":
    main()