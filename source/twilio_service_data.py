from twilio_api import tw_service_list, tw_func_list, tw_func_env_sids_list, tw_func_env_vars_list
import argparse
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="Twilio API URL")
parser.add_argument("account_sid", type=str, help="Twilio account SID")
parser.add_argument("auth_token", type=str, help="Twilio authentication token")
args = parser.parse_args()


def main():
    services_list = tw_service_list(args.url, args.account_sid, args.auth_token)
    if services_list:
        for service in services_list:
            print(f"Service_SID: {service["sid"]}, Service_unique_name: {service["u_name"]}")
            func_list = tw_func_list(args.url, args.account_sid, args.auth_token, service["sid"])
            for func in func_list:
                print(f"  Function_SID: {func["sid"]}, Function_name: {func["name"]}")
            env_list = tw_func_env_sids_list(args.url, args.account_sid, args.auth_token, service["sid"])
            for env in env_list:
                print(f"  Environment_SID: {env["sid"]}, Environment_domain: {env["domain"]}")
                var_list = tw_func_env_vars_list(args.url, args.account_sid, args.auth_token, service["sid"], env["sid"])
                for var in var_list:
                    print(f"    Variable_SID: {var["sid"]}, Variable_name: {var["name"]}")
    else:
        logger.info("There are no active services.")
        exit(1)


if __name__ == "__main__":
    main()