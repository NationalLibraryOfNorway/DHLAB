import requests

class DHLabApiError(requests.exceptions.HTTPError):
    pass

def validate_response_status(response: requests.Response) -> None:
    if response.status_code != 200:
        raise DHLabApiError(
            f"Status code: {response.status_code}: {response.reason}\n\n"
            + "There is an error connecting to the DHLab API. This is most likely not an error in your code,"
            + " but with the DHLab library or API. Try running the code again, and if that doesn't work, try to"
            + " reinstall/update the dhlab package (e.g. by running: 'pip install --upgrade dhlab').\nIf the error"
            + " persists, then please leave an issue at https://github.com/NationalLibraryOfNorway/DHLAB/issues/."
        )

def api_get(url: str, params: dict | None = None, session: requests.Session | None = None):
    if session is None:
        session = requests.Session()

    res = session.get(url, params=params)
    validate_response_status(res)

    return res

def api_post(url: str, json: dict | None = None, session: requests.Session | None = None):
    if session is None:
        session = requests.Session()

    res = session.post(url, json=json)
    validate_response_status(res)

    return res

