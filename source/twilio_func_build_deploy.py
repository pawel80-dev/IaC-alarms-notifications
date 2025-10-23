from twilio_api import tw_func_build_deploy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="Twilio API URL")
# parser.add_argument("code_url", type=str, help="Twilio Function code upload API URL")
parser.add_argument("account_sid", type=str, help="Twilio account SID")
parser.add_argument("auth_token", type=str, help="Twilio authentication token")
parser.add_argument("service_sid", type=str, help="Twilio service SID")
parser.add_argument("env_sid", type=str, help="Twilio environment SID")
parser.add_argument("build_sid", type=str, help="Twilio build SID")
args = parser.parse_args()


def main():
    tw_func_build_deploy(args.url, args.account_sid, args.auth_token, 
                         args.service_sid, args.env_sid, args.build_sid)


if __name__ == "__main__":
    main()