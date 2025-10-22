from twilio_api import (tw_service_list, tw_service_delete, tw_service_create, tw_service_build_sid, 
                        tw_func_create, tw_func_delete, tw_func_list, tw_func_version_list, tw_func_code_upload,
                        tw_func_build, tw_func_build_deploy, tw_func_create_env_var, tw_func_env_sids_list)
# import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="Twilio API URL")
# parser.add_argument("code_url", type=str, help="Twilio Function code upload API URL")
parser.add_argument("account_sid", type=str, help="Twilio account SID")
parser.add_argument("auth_token", type=str, help="Twilio authentication token")
args = parser.parse_args()

# Display logging info
# logging.basicConfig(level=logging.INFO)


##################### Twilio Function Deployment Steps: #####################
# 1. Create a service
# 2. Create a Function
# 3. Create environment variables (if needed and if they already do not exist)
# 4. Upload (update) your function code as a new Function Version
# 5. Create a new Build that includes your Function Version
# 6. Deploy the Build to your desired Environment


def main():
    tw_service_list(args.url, args.account_sid, args.auth_token)
    # tw_service_delete(url, account_sid, auth_token, service_sid)
    # service_sid = tw_service_create(url, account_sid, auth_token, service_name)
    # tw_service_build_sid(url, account_sid, auth_token, service_sid)
    # func_sid = tw_func_create(url, account_sid, auth_token, service_sid, func_name)
    # tw_func_list(url, account_sid, auth_token, service_sid)
    # func_version = tw_func_version_list(url, account_sid, auth_token, service_sid, func_sid)
    # tw_func_delete(url, account_sid, auth_token, service_sid, function_sid)
    # tw_func_code_upload(code_url, account_sid, auth_token, service_sid, func_sid, code_location)
    # func_build_sid = tw_func_build(url, account_sid, auth_token, service_sid, func_version)
    # tw_func_env_sids_list(url, account_sid, auth_token, service_sid)
    # tw_func_create_env_var(url, account_sid, auth_token, service_sid, env_sid, 
    #                        manager_user_key, manager_user_value)
    # tw_func_build_deploy(url, account_sid, auth_token, service_sid, env_sid, build_sid)


if __name__ == "__main__":
    main()