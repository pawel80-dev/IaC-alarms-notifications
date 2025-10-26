from twilio_api import tw_service_create, tw_func_create, tw_func_create_env
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="Twilio API URL")
parser.add_argument("account_sid", type=str, help="Twilio account SID")
parser.add_argument("auth_token", type=str, help="Twilio authentication token")
parser.add_argument("service_name", type=str, help="Twilio service name")
parser.add_argument("func_name", type=str, help="Twilio Function name")
parser.add_argument("env", type=str, help="Twilio Function environment type (dev, prod, etc.)")
args = parser.parse_args()


def main():
    service_sid = tw_service_create(args.url, args.account_sid, args.auth_token, args.service_name)
    tw_func_create(args.url, args.account_sid, args.auth_token, service_sid, args.func_name)
    tw_func_create_env(args.url, args.account_sid, args.auth_token, service_sid, args.env)


if __name__ == "__main__":
    main()