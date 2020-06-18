import os


from google.oauth2 import service_account


# DEFUALT_USER_EMAIL = 'contactclient@idesys.org'
DEFUALT_USER_EMAIL = 'nathan.seva@idesys.org'


SERVICE_ACCOUNT_FILE = 'idesysbot0-1591888101053-9a8cbb4621b4.json'
if not os.path.exists(SERVICE_ACCOUNT_FILE):
    try:
        GOOGLE_API_JSON_FILE = os.environ['GOOGLE_API_JSON_FILE']
    except KeyError:
        raise Exception('Provide Google API json file')
    else:
        with open(SERVICE_ACCOUNT_FILE, 'w') as my_file:
            my_file.writz(GOOGLE_API_JSON_FILE)


def get_delegated_credentials(scopes, user_email=None):
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=scopes)
    return credentials.with_subject(user_email or DEFUALT_USER_EMAIL)
