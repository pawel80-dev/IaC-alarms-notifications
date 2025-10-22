import requests
import logging
import json
# from urllib3.exceptions import InsecureRequestWarning

# logger will return the source module name
logger = logging.getLogger(__name__)
# display logging info level
logging.basicConfig(level=logging.INFO)

# Suppress certificate warnings
# requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


############################# Twilio Services #############################
def tw_service_list(tw_url: str, acc_id: str, token: str) -> None:
    logger.info("Twilio Service Listing...")

    response = requests.get(
        url=tw_url, 
        auth=(acc_id, token)
    )

    if response.status_code == 200:
        # logger.info(json.dumps(response.json(), indent=4))
        for service in response.json()["services"]:
            # logger.info(f'Service SID: {service["sid"]}, Service name: {service["friendly_name"]}')
            logger.info(f'Service SID: {service["sid"]}, Service name: {service["friendly_name"]}')
    else:
        logger.info("Failed to retrieve service list:", response.status_code)
        logger.info(response.text)


def tw_service_create(tw_url: str, acc_id: str, token: str, srv_name: str) -> str:
    data = {
        "FriendlyName": srv_name,
        "UniqueName": srv_name
    }
    logger.info("Twilio Service Creation...")

    try:
        response = requests.post(
            url=tw_url,
            data=data,
            auth=(acc_id, token)
        )
        response.raise_for_status()
        logger.info("Service created successfully!")
        logger.info(f'Service SID: {response.json()["sid"]}, Domain: {response.json()["domain_base"]}.twil.io')
        return response.json()["sid"]

    except requests.exceptions.HTTPError as err:
        logger.error(f"It is possible that service already exists: {err}")
        exit(1)


def tw_service_delete(tw_url: str, acc_id: str, token: str, srv_id: str) -> None:
    api = f"/{srv_id}"
    url = tw_url + api
    logger.info("Twilio Service Delete...")

    try:
        response = requests.delete(
            url=url,
            auth=(acc_id, token)
        )
        response.raise_for_status()
        logger.info("Service successfully deleted!")

    except requests.exceptions.HTTPError as err:
        logger.error(err)
        exit(1)


def tw_service_build_sid(tw_url: str, acc_id: str, token: str, srv_id: str) -> None:
    api = f"/{srv_id}/Builds?PageSize=1"
    url = tw_url + api
    logger.info("Service Build SID...")

    response = requests.get(
        url=url,
        auth=(acc_id, token)
    )

    if response.status_code == 200:
        logger.info("Service SID successfully retrieved!")
        logger.info(json.dumps(response.json(), indent=4))
    else:
        logger.info("Failed to retrieved service SID:", response.status_code)
        logger.info(response.text)


############################ Twilio Functions #############################
def tw_func_create(tw_url: str, acc_id: str, token: str, srv_id: str, func_name: str) -> str:
    api = f"/{srv_id}/Functions"
    url = tw_url + api
    data = {
        "FriendlyName": func_name,
    }
    logger.info("Twilio Function Creation...")

    response = requests.post(
        url=url,
        data=data,
        auth=(acc_id, token)
    )

    if response.status_code == 201:
        logger.info("Function created successfully!")
        logger.info(f'Function SID: {response.json()["sid"]}')
        return response.json()["sid"]
    else:
        logger.info("Failed to create function:", response.status_code)
        logger.info(response.text)


def tw_func_delete(tw_url: str, acc_id: str, token: str, srv_id: str, func_id: str) -> None:
    api = f"/{srv_id}/Functions/{func_id}"
    url = tw_url + api
    logger.info("Twilio Funciton Delete...")

    try:
        response = requests.delete(
            url=url,
            auth=(acc_id, token)
        )
        response.raise_for_status()
        logger.info("Function successfully deleted!")

    except requests.exceptions.HTTPError as err:
        logger.error(f"Function not found: {err}")
        exit(1)


def tw_func_list(tw_url: str, acc_id: str, token: str, srv_id: str) -> None:
    api = f"/{srv_id}/Functions"
    url = tw_url + api
    logger.info("Twilio Function list within a service...")

    response = requests.get(
        url=url,
        auth=(acc_id, token)
    )

    if response.status_code == 200:
        logger.info("Function list successfully retrieved!")
        for func in response.json()["functions"]:
            logger.info(f'Function SID: {func["sid"]}, Function name: {func["friendly_name"]}')
        # logger.info(json.dumps(response.json(), indent=4))
        # return json.dumps(response.json(), indent=4)
    else:
        logger.info("Failed to create function:", response.status_code)
        logger.info(response.text)


def tw_func_code_upload(tw_url: str, acc_id: str, token: str, srv_id: str, func_id: str, file_name: str) -> str:
    api = f"/{srv_id}/Functions/{func_id}/Versions"
    url = tw_url + api
    files = {
        "Path": (None, "/api"), 
        "Visibility": (None, "public"), 
        "Content": (file_name, open(file_name, "rb"), "application/javascript")
    }
    logger.info("Twilio Function Creation...")

    response = requests.post(
        url=url,
        files=files,
        auth=(acc_id, token)
    )

    if response.status_code == 201:
        logger.info("Function code uploaded successfully!")
        logger.info(f'Function Version SID: {response.json()["sid"]}')
        return response.json()["sid"]
    else:
        logger.info("Failed to upload function code:", response.status_code)
        logger.info(response.text)


def tw_func_version_list(tw_url: str, acc_id: str, token: str, srv_id: str, func_id: str) -> str:
    api = f"/{srv_id}/Functions/{func_id}/Versions"
    url = tw_url + api
    logger.info("Twilio Function versions list...")

    try:
        response = requests.get(
            url=url,
            auth=(acc_id, token)
        )
        response.raise_for_status()
        # First element on the list is the latest version!
        if response.status_code == 200 and response.json()["function_versions"] != []:
            logger.info("Twilio Function versions list successfully retrieved!")
            logger.info(f'Latest Function version SID: {response.json()["function_versions"][0]["sid"]}')
            return response.json()["function_versions"][0]["sid"]
        
        elif response.status_code == 200 and response.json()["function_versions"] == []:
            logger.error("Function version list is empty!")
    
    except requests.exceptions.HTTPError as err:
        logger.error(err)
        exit(1)
    # else:
    #     logger.info("Failed to retrieved Twilio Function versions list:", response.status_code)
    #     logger.info(response.text)


def tw_func_build(tw_url: str, acc_id: str, token: str, srv_id: str, func_ver: str) -> str:
    api = f"/{srv_id}/Builds"
    url = tw_url + api
    data = {
        "FunctionVersions": func_ver,
        "AssetVersions": [],
        "Runtime": "node22"
    }
    logger.info("Twilio Function Build...")

    response = requests.post(
        url=url,
        data=data,
        auth=(acc_id, token)
    )

    if response.status_code == 201:
        logger.info("Function build successfully created!")
        logger.info(f'Function build SID: {response.json()["sid"]}')
        return response.json()["sid"]
    else:
        logger.info("Failed to build a function:", response.status_code)
        logger.info(response.text)


def tw_func_build_deploy(tw_url: str, acc_id: str, token: str, srv_id: str, env_id: str, build_id: str) -> str:
    api = f"/{srv_id}/Environments/{env_id}/Deployments"
    url = tw_url + api
    data = {
        "BuildSid": build_id
    }
    logger.info("Twilio Function build deployment...")

    try:
        response = requests.post(
            url=url,
            data=data,
            auth=(acc_id, token)
        )

        response.raise_for_status()
        logger.info("Function build deployed successfully!")
        logger.info(f'Function deploy SID: {response.json()["sid"]}')
        return response.json()["sid"]
    # except requests.exceptions.HTTPError as err:
    except Exception:
        logger.error(response.text)
        exit(1)


##################### Twilio Function Env Variables #######################
def tw_func_env_sids_list(tw_url: str, acc_id: str, token: str, srv_id: str) -> None:
    api = f"/{srv_id}/Environments"
    url = tw_url + api
    logger.info("Twilio Environment SIDs list...")

    response = requests.get(
        url=url,
        auth=(acc_id, token)
    )

    if response.status_code == 200:
        logger.info("Environment SIDs successfully retrieved!")
        #logger.info(json.dumps(response.json(), indent=4))
        # return response.json()["sid"]
        for env in response.json()["environments"]:
            logger.info(f'Environment SID: {env["sid"]}')
    else:
        logger.info("Failed to read environment SIDs:", response.status_code)
        logger.info(response.text)


def tw_func_create_env_var(tw_url: str, acc_id: str, token: str, srv_id: str, env_id: str, 
                           key: str, value: str) -> str:
    api = f"/{srv_id}/Environments/{env_id}/Variables"
    url = tw_url + api
    data = {
        "Key": key,
        "Value": value
    }
    logger.info("Twilio Environment Variable...")

    try:
        response = requests.post(
            url=url,
            data=data,
            auth=(acc_id, token)
        )
        response.raise_for_status()
        logger.info("Environment variable created successfully!")
        logger.info(f'Environment variable SID: {response.json()["sid"]}')
        return response.json()["sid"]
    except requests.exceptions.HTTPError as err:
        logger.error(f"Same variable might already exists: {err}")
        exit(1)


def tw_func_update_env_var(tw_url: str, acc_id: str, token: str, srv_id: str, env_id: str, var_id: str, 
                           key: str, value: str) -> str:
    api = f"/{srv_id}/Environments/{env_id}/Variables/{var_id}"
    url = tw_url + api
    data = {
        "Key": key,  # optional, use for key rename
        "Value": value
    }
    logger.info("Twilio Environment variable update...")

    response = requests.post(
        url=url,
        data=data,
        auth=(acc_id, token)
    )

    if response.status_code == 200:
        logger.info("Environment variable successfully updated!")
        # logger.info(json.dumps(response.json(), indent=4))
        logger.info(f'Variable SID: {response.json()["sid"]}')
        return response.json()["sid"]
    else:
        logger.info("Failed to update environment variable:", response.status_code)
        logger.info(response.text)


def tw_func_env_vars_list(tw_url: str, acc_id: str, token: str, srv_id: str, env_id: str) -> None:
    api = f"/{srv_id}/Environments/{env_id}/Variables"
    url = tw_url + api
    logger.info("Twilio Environment variables list...")

    response = requests.get(
        url=url,
        auth=(acc_id, token)
    )

    if response.status_code == 200:
        logger.info("Environment variable list successfully created!")
        # logger.info(json.dumps(response.json(), indent=4))
        # return response.json()["sid"]
        for var in response.json()["variables"]:
            logger.info(f'Environment var name: {var["key"]}, Environment var SID: {var["sid"]}')
    else:
        logger.info("Failed to create environment variable list:", response.status_code)
        logger.info(response.text)


def tw_func_delete_env_var(tw_url: str, acc_id: str, token: str, srv_id: str, env_id: str, var_id: str) -> None:
    api = f"/{srv_id}/Environments/{env_id}/Variables/{var_id}"
    url = tw_url + api
    logger.info("Twilio Environment variable delete...")

    response = requests.delete(
        url=url,
        auth=(acc_id, token)
    )

    if response.status_code == 204:
        logger.info("Environment variable successfully deleted!")
    else:
        logger.info("Failed to delete environment variable:", response.status_code)
        logger.info(response.text)


if __name__ == "__main__":
    print("Used for testing the code")
    # tw_service_list(url, account_sid, auth_token)
    # tw_service_delete(url, account_sid, auth_token, service_sid)
    # tw_service_create(url, account_sid, auth_token, service_name)
    # tw_func_create(url, account_sid, auth_token, service_sid, function_name)
    # tw_func_delete(url, account_sid, auth_token, service_sid, function_sid)
    # tw_func_version_list(url, account_sid, auth_token, service_sid, function_sid)
    # tw_func_build(url, account_sid, auth_token, service_sid, function_version)
    # tw_func_build_deploy(url, account_sid, auth_token, service_sid, env_sid, build_sid)
    # tw_service_build_sid(url, account_sid, auth_token, service_sid)
    # tw_func_code_upload(code_url, account_sid, auth_token, service_sid, function_sid, "source/alarm_func.js")
    # tw_func_env_sids_list(url, account_sid, auth_token, service_sid)
    # tw_func_create_env_var(url, account_sid, auth_token, service_sid, env_sid, 
    #                        manager_pass_key, manager_pass_value)
    # tw_func_update_env_var(url, account_sid, auth_token, service_sid, env_sid, key1_sid, 
    #                     manager_pass_key, manager_pass_value)
    # tw_func_env_vars_list(url, account_sid, auth_token, service_sid, env_sid)
    # tw_func_delete_env_var(url, account_sid, auth_token, service_sid, env_sid, key1_sid)
