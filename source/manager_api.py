import requests
import logging
import random
from urllib3.exceptions import InsecureRequestWarning

# Logging on the INFO level
logging.basicConfig(level=logging.INFO)

# Suppress certificate warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

manager_url = ""
login = ""
password = ""


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


def alarm_notification(manager_url: str, jsession_id: str, manager_token: str, 
                       webhook_user: str, webhook_pass: str, webhook_url: str) -> None:
    api = "/dataservice/notifications/rule"
    url = manager_url + api
    headers = {
        "Content-Type": "application/json",
        "Cookie": jsession_id,
        "X-XSRF-TOKEN": manager_token
    }
    payload = {
        "notificationRuleName": "IntStatusChanged",
        "severity": "Medium",
        "alarmName": "Interface_State_Change",
        "accountDetails": "noreply@cisco.com",
        "webHookEnabled": True,
        "webhookUsername": webhook_user,
        "webhookPassword": webhook_pass,
        "webhookUrl": webhook_url,
        "updatedBy": "no_admin",
        "devicesAttached": "C8200-1N-4T-FGL2540LAEM, C8200-1N-4T-FGL2540LAWH",
        # "devicesAttached": ["C8200-1N-4T-FGL2540LAWH"],
        "emailThreshold": 5,
        "accountDetailsArray": [
          "noreply@cisco.com"
        ]
    }
    response = requests.post(url=url, headers=headers, json=payload, verify=False)
    if response.status_code != 202:
        logging.info(f"Manager alarm notification failed: {response.status_code} {response.text}")
        return None
    else:
        logging.info("Manager alarm notification set correctly!")
        return None


def main() -> None:
    # manager_connectivity_test(manager_url)
    session_id = manager_jsession_id(manager_url, login, password)
    token = manager_token(manager_url, session_id)
    alarm_notification(manager_url, session_id, token)
    manager_logout(manager_url, session_id)


if __name__ == "__main__":
    main()