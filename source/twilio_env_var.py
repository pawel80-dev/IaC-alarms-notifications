from twilio_api import tw_func_env_vars_list, tw_func_create_env_var, tw_func_update_env_var
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="Twilio API URL")
parser.add_argument("account_sid", type=str, help="Twilio account SID")
parser.add_argument("auth_token", type=str, help="Twilio authentication token")
parser.add_argument("service_sid", type=str, help="Twilio service SID")
parser.add_argument("env_sid", type=str, help="Twilio environment SID")
parser.add_argument("var_key", type=str, help="Twilio environment variable key")
parser.add_argument("var_value", type=str, help="Twilio environment variable value")
args = parser.parse_args()


def main():
    var_list = tw_func_env_vars_list(args.url, args.account_sid, args.auth_token, 
                                     args.service_sid, args.env_sid)
    # if variable already exists, it will be updated
    for var in var_list:
        if args.var_key == var["name"]:
            tw_func_update_env_var(args.url, args.account_sid, args.auth_token, 
                                   args.service_sid, args.env_sid, var["sid"], args.var_key, args.var_value)
            exit(0)

    # if variable doesn't exist, it will be created
    tw_func_create_env_var(args.url, args.account_sid, args.auth_token, args.service_sid, 
                           args.env_sid, args.var_key, args.var_value)


if __name__ == "__main__":
    main()