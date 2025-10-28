from manager_api import (manager_connectivity_test, manager_jsession_id, manager_token, manager_logout,
                        alarm_notification)
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="Manager API URL")
parser.add_argument("username", type=str, help="Manager API username")
parser.add_argument("password", type=str, help="Manager API password")
parser.add_argument("wh_user", type=str, help="Manager webhook username")
parser.add_argument("wh_pass", type=str, help="Manager webhook password")
parser.add_argument("wh_url", type=str, help="Manager webhook URL")
args = parser.parse_args()


def main():
    # manager_connectivity_test(args.url)
    session_id = manager_jsession_id(args.url, args.username, args.password)
    token = manager_token(args.url, session_id)
    alarm_notification(args.url, session_id, token, args.wh_user, args.wh_pass, args.wh_url)
    manager_logout(args.url, session_id)


if __name__ == "__main__":
    main()