from twilio_api import tw_service_delete
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="Twilio API URL")
parser.add_argument("account_sid", type=str, help="Twilio account SID")
parser.add_argument("auth_token", type=str, help="Twilio authentication token")
parser.add_argument("service_sid", type=str, help="Twilio service SID")
args = parser.parse_args()


def main():
    tw_service_delete(args.url, args.account_sid, args.auth_token, args.service_sid) 


if __name__ == "__main__":
    main()