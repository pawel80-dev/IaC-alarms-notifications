from twilio_api import tw_func_code_upload, tw_func_build, tw_func_build_deploy
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="Twilio API URL")
parser.add_argument("code_url", type=str, help="Twilio function code upload API URL")
parser.add_argument("account_sid", type=str, help="Twilio account SID")
parser.add_argument("auth_token", type=str, help="Twilio authentication token")
parser.add_argument("service_sid", type=str, help="Twilio service SID")
parser.add_argument("func_sid", type=str, help="Twilio function SID")
parser.add_argument("env_sid", type=str, help="Twilio environment SID")
parser.add_argument("code_location", type=str, help="Twilio Node.JS code path")
args = parser.parse_args()


def main():
    func_version_sid = tw_func_code_upload(args.code_url, args.account_sid, args.auth_token, 
                                           args.service_sid, args.func_sid, args.code_location)
    func_build_sid = tw_func_build(args.url, args.account_sid, args.auth_token, 
                                   args.service_sid, func_version_sid)
    time.sleep(10)
    tw_func_build_deploy(args.url, args.account_sid, args.auth_token, 
                         args.service_sid, args.env_sid, func_build_sid)


if __name__ == "__main__":
    main()