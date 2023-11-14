import os
import requests
from time import sleep
import xmltodict


def request(url) -> list[dict]:
    arqv = []
    flag = True
    while flag:
        try:
            response = requests.get(url)
        except TimeoutError:
            print("Timeout: sleeping for 60 secs")
            sleep(60)
            continue
        except requests.exceptions.ConnectTimeout:
            print("Timeout: sleeping for 60 secs")
            sleep(60)
            continue
        except requests.exceptions.Timeout:
            print("Timeout: sleeping for 60 secs")
            sleep(60)
            continue
        except requests.exceptions.ConnectionError:
            print("ConnectionError: sleeping for 60 secs")
            sleep(60)
            continue
        if response.status_code == 200:
            if "xml" in response.headers["Content-Type"]:
                resp = xmltodict.parse(response.content)["xml"]
            else:
                resp = response.json()
            if isinstance(resp["dados"], list):
                arqv += resp["dados"]
            else:
                arqv.append(resp["dados"])
            try:
                rels = [link["rel"] for link in resp["links"]]
            except:
                rels = [link["rel"] for link in resp["links"]["link"]]
            if "next" in rels:
                url = resp["links"][rels.index("next")]["href"]
            else:
                flag = False
        else:
            raise ConnectionError(response.status_code)
    return arqv


def create_folder_if_not_exists(folder_path):
    """
    Check if a folder exists, and create it if it doesn't.

    Parameters:
    - folder_path (str): Path of the folder to check and create.

    Returns:
    - None
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")


from datetime import datetime, timedelta


def generate_dates(start_date, end_date, step=1, **kwargs):
    """
    Generate dates between a start date and an end date with a specified step size.

    Parameters:
    - start_date (str or datetime): Start date in 'YYYY-MM-DD' format or as a datetime object.
    - end_date (str or datetime): End date in 'YYYY-MM-DD' format or as a datetime object.
    - step (int): Number of days between consecutive dates (default is 1).

    Returns:
    - list of datetime objects representing the generated dates.
    """
    input_format = kwargs.get("input_format", "%Y-%m-%d")
    output_format = kwargs.get("output_format", "%Y-%m-%d")
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, input_format)
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, input_format)

    current_date = start_date
    dates = []

    while current_date <= end_date:
        dates.append(current_date.strftime(output_format))
        current_date += timedelta(days=step)

    return dates
