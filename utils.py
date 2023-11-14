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
