import json
import requests
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


org_name = "arabbank-test"
base_url = "https://api.enterprise.apigee.com/v1/organizations/arabbank-test"
oauth_url = "https://arab-bank-plc-gw.login.apigee.com/oauth/token"
SAML = "vQTRbmqCbQvN8jJqoqvrMNYlpFAyoSaA"
# https://arab-bank-plc-gw.login.apigee.com/passcode

def oauth():
    d = {'grant_type': 'password', 'username': user_name,
         'password': password, 'passcode': SAML}
    r = requests.post(oauth_url, data=d, headers={'Authorization': 'Basic ZWRnZWNsaTplZGdlY2xpc2VjcmV0',
                      'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'Accept': 'application/json;charset=utf-8'}, verify=False)
    # print(r.json())
    # print(json.dumps(r.json(), indent=2))
    response = json.loads(r.text)
    return (response["access_token"])


def get_proxies():
    proxies_url = base_url + "/apis/"
    r = requests.get(proxies_url, headers={
                     "Authorization": f"Bearer {access_token}"}, verify=False, )
    apis = json.loads(r.text)
    return apis


def get_proxy_latest_revision(proxy):
    revision_url = base_url + f"/apis/{proxy}/revisions/"
    r = requests.get(revision_url, headers={
                     "Authorization": f"Bearer {access_token}"}, verify=False)
    response = json.loads(r.text)
    revision = response[-1]
    return revision

def get_proxy_endpoint_name(proxy, revision):
    endpoint_url = base_url + f"/apis/{proxy}/revisions/{revision}/proxies/"
    r = requests.get(endpoint_url, headers={
                     "Authorization": f"Bearer {access_token}"}, verify=False)
    response = json.loads(r.text)
    endpoint_name = response[0]
    return endpoint_name

def get_apis_proxies_basepath(proxy, revision, endpoint):
    basepath_url = base_url + f"/apis/{proxy}/revisions/{revision}/proxies/{endpoint}/"
    r = requests.get(basepath_url, headers={
                     "Authorization": f"Bearer {access_token}"}, verify=False)
    response = json.loads(r.text)
    basepath = response
    return basepath

try:
    access_token = oauth()
    proxies = get_proxies()
    # proxies = ['APIGEE-HYBRID-DEMO' ,'OCR', 'ArabiPay-E2EKey-API']
    with open("collection.txt", "a+") as file:
        for proxy in proxies:
            revision = get_proxy_latest_revision(proxy)
            endpoint = get_proxy_endpoint_name(proxy, revision)
            basepath = get_apis_proxies_basepath(proxy, revision, endpoint)
            # print(basepath)
            # file.writelines(f"Proxy name: {proxy} ----> Basepath: {basepath['connection']['basePath']}\n")
            file.write(f"{proxy}, Basepath: {basepath['connection']['basePath']},\n")
            if basepath['flows']:
                for item in range(len(basepath['flows'])):
                    # print(basepath['flows'].count("proxy.pathsuffix"))
                    # print(len(basepath['flows']))
                    # print(basepath['flows'])
                    try: 
                        # file.writelines(f"{basepath['flows'][item]['condition']}\n")
                        # print((f"{basepath['connection']['basePath']+re.search('/[a-z]*',basepath['flows'][item]['condition']).group(0)},{re.search('verb = .(.*)',basepath['flows'][item]['condition']).group(1)}\n,"))
                        # file.write(f"{basepath['connection']['basePath']+re.search('/[a-z]*',basepath['flows'][item]['condition']).group(0)},{re.search('verb =* .([A-Z]*)',basepath['flows'][item]['condition']).group(1)}\n, ")
                        file.write(f", ,{basepath['flows'][item]['condition']}\n")
                    except KeyError as error:
                        print(error, "1")
                        print(proxy)
                        # print(proxy, revision)

                    except AttributeError as exception:
                        print(exception, "2")
                        print(proxy)
                        print(f"{basepath['flows'][item]}")
                        if (re.search('/[a-z]*',basepath['flows'][item]['condition'])):
                            print(f"{basepath['connection']['basePath']+re.search('/[a-z]*',basepath['flows'][item]['condition']).group(0)}, ALL, ")
                    except Exception as exception:
                        print(exception, "3")
            file.write("\n")
except KeyError as error:
    print(error)
    print(basepath)
    print(proxy, revision)

except requests.exceptions.ProxyError as error:
    print(error, "6")

except requests.exceptions.TooManyRedirects as error:
    print (error, '9')

except Exception as error:
    print(error, "7")