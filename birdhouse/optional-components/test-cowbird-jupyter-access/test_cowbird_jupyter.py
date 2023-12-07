"""
Script used to setup a test user along with different test files, for the test notebooks from the
 `PAVICS-e2e-workflow-test` repo :

- https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/blob/master/notebooks-auth/test_cowbird_jupyter.ipynb
- https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/blob/master/notebooks-auth/resources/user_test_cowbird_jupyter.ipynb
"""

import json
import os
import requests
import shutil
import time
import urllib3
from pathlib import Path

print("Setup configuration parameters...")

TIMEOUT_DELAY = 5
MAX_ATTEMPTS = 8

VERIFY_SSL = False
if not VERIFY_SSL:
    urllib3.disable_warnings()  # disable warnings for using https without certificate verification enabled
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}
PAVICS_HOST_URL = os.getenv("PAVICS_HOST_URL")

COWBIRD_URL = f"{PAVICS_HOST_URL}/cowbird"
MAGPIE_URL = f"{PAVICS_HOST_URL}/magpie"

WPS_OUTPUTS_DIR = os.getenv("WPS_OUTPUTS_DIR")
WORKSPACE_DIR = os.getenv("WORKSPACE_DIR")

print(f"  wps_outputs_dir : {WPS_OUTPUTS_DIR}")
print(f"  workspace_dir : {WORKSPACE_DIR}")

def get_credentials(var_name):
    value = os.getenv(var_name)
    if not value:
        raise ValueError("Missing test admin credentials `{}` to run tests.".format(var_name))
    return value

TEST_MAGPIE_ADMIN_USERNAME = get_credentials("MAGPIE_ADMIN_USERNAME")
TEST_MAGPIE_ADMIN_PASSWORD = get_credentials("MAGPIE_ADMIN_PASSWORD")

TEST_COWBIRD_JUPYTERHUB_USERNAME = os.getenv("TEST_COWBIRD_JUPYTERHUB_USERNAME")
TEST_COWBIRD_JUPYTERHUB_PASSWORD = os.getenv("TEST_COWBIRD_JUPYTERHUB_PASSWORD")

print("  Verify SSL : {}".format(VERIFY_SSL))
print("  Will use Magpie URL:   [{}]".format(MAGPIE_URL))

def response_msg(message, response, is_json=True):
    """Append useful response details to provided message."""
    _body = response.text
    _detail = "<unknown>"
    if is_json:
        try:
            _body = response.json()
            _detail = _body.get("detail", _body.get("message", "<unknown>"))
        except json.JSONDecodeError:
            # ignore and revert to text body since it could not be parsed as JSON
            _body = response.text
    return "{} Response replied with ({}) [{}]\nContent: {}\n\n".format(message, response.status_code, _detail, _body)

def magpie_signin(user_name, password):
    signin_url = f"{MAGPIE_URL}/signin"
    data = {"user_name": user_name, "password": password}
    try:
        resp = requests.request(url=signin_url, headers=HEADERS, method="POST", json=data, timeout=10, verify=VERIFY_SSL)
    except Exception as exc:
        raise RuntimeError(f"Failed to sign in to Magpie (url: `{signin_url}`) with user `{data['user_name']}`. "
                           f"Exception : {exc}. ")
    if resp.status_code != 200:
        raise RuntimeError(f"Unexpected response while trying to sign in to Magpie with user `{user_name}` : {resp.text}")
    return resp

def create_magpie_user(user_name, password, session):
    user_data = {"user_name": user_name,
                 "email": f"{user_name}@user.com",
                 "password": password,
                 "group_name": "users"}
    resp = magpie_admin_session.post(url=f"{MAGPIE_URL}/users", json=user_data, allow_redirects=False)
    if resp.status_code != 201:
        raise ValueError(response_msg("\nCould not create test user [{}]".format(user_name), resp))
    session.cookies = magpie_signin(user_name, password).cookies
    return resp.json()

# Make sure Cowbird is running before creating user
for svc_name, svc_url in [("Magpie", MAGPIE_URL),
                          ("Cowbird", COWBIRD_URL)]:
    resp = None
    for i in range(MAX_ATTEMPTS):
        time.sleep(i * TIMEOUT_DELAY)
        try:
            resp = requests.get(svc_url, verify=VERIFY_SSL)
            assert resp.status_code == 200
            print(f"{svc_name} availability checked successfully.")
            break
        except Exception as exc:
            print(f"Failed to connect to {svc_name} [{exc}]. \nAttempting again ({i + 1})...")
    else:
        raise ConnectionError("Failed to connect to {} on url {}".format(svc_name, svc_url))

# ------------------------------------------------------------------
magpie_admin_session = requests.Session()
magpie_admin_session.verify = VERIFY_SSL
magpie_admin_session.headers = HEADERS
magpie_admin_session.cookies = magpie_signin(TEST_MAGPIE_ADMIN_USERNAME, TEST_MAGPIE_ADMIN_PASSWORD).cookies

test_user_session = requests.Session()
test_user_session.verify = VERIFY_SSL
test_user_session.headers = HEADERS

# ------------------------------------------------------------------
print("Creating test user on Magpie...")
test_user_id = create_magpie_user(TEST_COWBIRD_JUPYTERHUB_USERNAME, TEST_COWBIRD_JUPYTERHUB_PASSWORD, test_user_session)["user"]["user_id"]

user_workspace_dir = f"{WORKSPACE_DIR}/{TEST_COWBIRD_JUPYTERHUB_USERNAME}"

# Make sure cowbird had time to create user workspace before executing following operations
for i in range(MAX_ATTEMPTS):
    time.sleep(i * TIMEOUT_DELAY)
    if os.path.exists(user_workspace_dir):
        print(f"User workspace successfully found at path `{user_workspace_dir}`.")
        break
    print(f"Failed to find user workspace at path [{user_workspace_dir}]. Attempting again ({i + 1})...")
else:
    raise ConnectionError("Failed to create user workspace  to Cowbird on url {}".format(COWBIRD_URL))

# ------------------------------------------------------------------
# Add Geoserver shapefiles to the user workspace
print("Copying shapefile data to user workspace...")
GEOSERVER_TEST_DATA_DIR = "/geoserver-test-data"
for filename in os.listdir(GEOSERVER_TEST_DATA_DIR):
    file = Path(filename)
    stem, ext = file.stem, file.suffix
    # Make one read-only and one read-write copy
    for target_path, perms in [(os.path.join(f"{user_workspace_dir}/shapefile_datastore", f"{stem}_ro{ext}"), 0o664),
                               (os.path.join(f"{user_workspace_dir}/shapefile_datastore", f"{stem}_rw{ext}"), 0o666)]:
        shutil.copy2(os.path.join(GEOSERVER_TEST_DATA_DIR, filename), target_path)
        os.chmod(target_path, perms)

# ------------------------------------------------------------------
# Add wps-outputs
print("Creating test WPS outputs data...")
# Add public file
public_wpsoutputs_filepath = f"{WPS_OUTPUTS_DIR}/weaver/public/3dc704a8-e1f6-4fe8-8bf0-153cf1e52c7a/output/test_public_file.txt"
os.makedirs(os.path.dirname(public_wpsoutputs_filepath), exist_ok=True)
Path(public_wpsoutputs_filepath).touch()

# Check user permissions on WPS outputs user data
resp = None
for i in range(MAX_ATTEMPTS):
    time.sleep(i * TIMEOUT_DELAY)
    try:
        resp = magpie_admin_session.get(f"{MAGPIE_URL}/services/secure-data-proxy")
        break
    except Exception as exc:
        # Magpie is sometimes unaccessible even after the initial checkup and user creation,
        # so apply checks and attempts again
        print(f"Exception received when attempting to check for the `secure-data-proxy` service : \n{repr(exc)}\n"
              f"Attempting again ({i + 1})...")
else:
    raise ConnectionError("Failed to connect to Magpie on url {}".format(f"{MAGPIE_URL}/services/secure-data-proxy"))

if resp.status_code == 200:
    print("Secure-data-proxy service exists. Checking that the user has access to the wpsoutputs resource...")
    svc_id = resp.json()["service"]["resource_id"]

    resp = magpie_admin_session.get(f"{MAGPIE_URL}/users/{TEST_COWBIRD_JUPYTERHUB_USERNAME}/resources/{svc_id}/permissions?effective=true")
    if resp.status_code != 200:
        raise ValueError(response_msg("\nCould not get the secure-data-proxy resource permissions for the user.", resp))
    if "read-allow-match" not in resp.json()["permission_names"]:
        print("User does not have access to secure-data-proxy service. Adding read permission...")
        resp = magpie_admin_session.post(f"{MAGPIE_URL}/users/{TEST_COWBIRD_JUPYTERHUB_USERNAME}/resources/{svc_id}/permissions",
                                         json={"permission": {
                                             "name": "read",
                                             "access": "allow",
                                             "scope": "recursive"
                                         }})
        if resp.status_code != 201:
            raise ValueError(response_msg("\nFailed to add secure-data-proxy permission to the test user.", resp))
    print("User access to secure-data-proxy is allowed.")
elif resp.status_code == 404:
    print("No secure-data-proxy service found. The user should have access to the wpsoutputs resource by default.")
else:
    raise ValueError(response_msg("\nCould not find secure-data-proxy service.", resp))

# Add user specific file
user_wpsoutputs_filepath = f"{WPS_OUTPUTS_DIR}/weaver/users/{test_user_id}/test_user_file.txt"
os.makedirs(os.path.dirname(user_wpsoutputs_filepath), exist_ok=True)

Path(user_wpsoutputs_filepath).touch()

# Make sure cowbird has created the user WPS outputs hardlink successfuly before continuing with the tests.
expected_user_wps_outputs_hardlink = f"{user_workspace_dir}/wps_outputs/weaver/test_user_file.txt"
for i in range(MAX_ATTEMPTS):
    time.sleep(i * TIMEOUT_DELAY)
    if os.path.exists(expected_user_wps_outputs_hardlink):
        print(f"User WPS outputs hardlink successfully found at path `{expected_user_wps_outputs_hardlink}`.")
        break
    print(f"Failed to find user hardlink at path [{expected_user_wps_outputs_hardlink}]. Attempting again ({i + 1})...")
else:
    raise RuntimeError(f"Failed to create `{expected_user_wps_outputs_hardlink}` hardlink in the user workspace.")

print("Test setup completed.")
