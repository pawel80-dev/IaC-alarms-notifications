import requests
import logging
import random
import json
from urllib3.exceptions import InsecureRequestWarning

# Logging on the INFO level
logging.basicConfig(level=logging.INFO)

# Suppress certificate warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


manager_url = ""
login = ""
password = ""
my_uuid = ""
hostname = ""


def manager_connectivity_test(manager_url: str) -> None:
    response = requests.get(url=manager_url, verify=False)
    if response.status_code != 200:
        logging.info(f"Manager connectivity test error code: {response.status_code} {response.text}")
        return None
    else:
        logging.info("Manager connectivity test - successful!")
        return None


def manager_jsession_id(manager_url: str, login: str, password: str) -> str:
    api = "/j_security_check"
    url = manager_url + api
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "j_username": login, 
        "j_password": password
    }
    response = requests.post(url=url, headers=headers, data=payload, verify=False)
    if response.status_code != 200:
        logging.info(f"Manager jsession_id error code: {response.status_code} {response.text}")
        return None
    else:
        logging.info("Manager jsession_id - successful!")
        cookies = response.headers["Set-Cookie"]
        jsessionid = cookies.split(";")
        return jsessionid[0]


def manager_token(manager_url: str, jsession_id: str) -> str:
    api = "/dataservice/client/token"
    url = manager_url + api
    headers = {
        "Content-Type": "application/json",
        "Cookie": jsession_id
    }
    response = requests.get(url=url, headers=headers, verify=False)
    if response.status_code != 200:
        logging.info(f"Manager token error code: {response.status_code} {response.text}")
        return None
    else:
        logging.info("Manager token - successful!")
        return response.text


def manager_logout(manager_url: str, jsession_id: str) -> None:
    api = f"/logout?nocache={random.randint(1000, 9999)}"
    url = manager_url + api
    headers = {
        "Cookie": jsession_id
    }
    response = requests.post(url=url, headers=headers, verify=False)
    if response.status_code != 200:
        logging.info(f"Manager logout error code: {response.status_code} {response.text}")
        return None
    else:
        logging.info("Manager logout - successful!")
        return None


def manager_device_list(manager_url: str, jsession_id: str, manager_token: str) -> list:
    api = "/dataservice/system/device/vedges"
    url = manager_url + api
    headers = {
        "Content-Type": "application/json",
        "Cookie": jsession_id,
        "X-XSRF-TOKEN": manager_token
    }
    response = requests.get(url=url, headers=headers, verify=False)
    if response.status_code != 200:
        logging.info(f"Manager device list error code: {response.status_code} {response.text}")
        return None
    else:
        logging.info("Manager device list - successful!")
        # logging.info(f"Device list:\n {json.dumps(response.json()["data"], indent=4)}")
        return response.json()["data"]


def find_device(dev_list: list, hostname: str) -> str:
    for device in dev_list:
        if "configuredHostname" in device and device["configuredHostname"] == hostname:
            logging.info(f"Device {hostname} was found, its UUID is: {device['uuid']} - successful!")
            return device["uuid"]
    logging.info(f"Device {hostname} - not found!")
    return None


# API:
# Configuration - Device Inventory /system/device/bootstrap/device/{uuid}
def manager_bootstrap_gen(manager_url: str, jsession_id: str, manager_token: str, uuid: str) -> None:
    cfg_type = "cloudinit"
    include_root_cert = "true"
    # version = "v1"
    # api = f"/dataservice/system/device/bootstrap/device/{uuid}?configtype={cfg_type}&inclDefRootCert={include_root_cert}&version={version}"
    api = f"/dataservice/system/device/bootstrap/device/{uuid}?configtype={cfg_type}&inclDefRootCert={include_root_cert}"
    url = manager_url + api
    headers = {
        "Content-Type": "application/json",
        "Cookie": jsession_id,
        "X-XSRF-TOKEN": manager_token
    }
    response = requests.get(url=url, headers=headers, verify=False)
    if response.status_code != 200:
        logging.info(f"Manager bootstrap generate error code: {response.status_code} {response.text}")
        return None
    else:
        logging.info("Manager bootstrap generate - successful!")
        return response.json()["bootstrapConfig"]


def main() -> None:
    # manager_connectivity_test(manager_url)
    session_id = manager_jsession_id(manager_url, login, password)
    token = manager_token(manager_url, session_id)
    device_list = manager_device_list(manager_url, session_id, token)
    device_uuid = find_device(device_list, hostname)
    bootstrap_file = manager_bootstrap_gen(manager_url, session_id, token, device_uuid)
    logging.info(bootstrap_file)
    manager_logout(manager_url, session_id)


if __name__ == "__main__":
    main()