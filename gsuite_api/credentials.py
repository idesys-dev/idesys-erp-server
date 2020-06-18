from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = 'idesysbot0-1591888101053-9a8cbb4621b4.json'
# DEFUALT_USER_EMAIL = 'contactclient@idesys.org'
DEFUALT_USER_EMAIL = 'nathan.seva@idesys.org'

def get_delegated_credentials(scopes, user_email=None):
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=scopes)
    return credentials.with_subject(user_email or DEFUALT_USER_EMAIL)
