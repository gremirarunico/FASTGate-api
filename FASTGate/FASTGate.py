import requests
import datetime
from os.path import join
from os import getenv
from urllib.parse import quote
import json


class FASTGate:
    def __init__(self, username, password, ip='192.168.1.254'):
        self.username = username
        self.password = password
        self.ip = ip
        self.verbose = 0
        self.sessionFile = join(getenv("HOME"), 'FASTGateSession.json')
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
            'X-XSS-Protection': '1'
        }
        self.retry = 1

    # in verbose mode print data
    def __dep(self, data):
        if(self.verbose):
            print(data)

    # get the current timestamp (integer)
    def __now(self):
        return (int(datetime.datetime.now().timestamp()))

    # create the url in the proper way liked by the fastgate
    # address is the address of the fastgate, default 192.168.1.254
    # attributes is a dictionary with GET request
    # t choice if print ?_t=timestamp insthead of ?_=timestamp (is a secure feature due to angular.js)
    # arg if is 0 send the url clean without any GET request
    def __urlFormer(self, address, attributes, t=0, args=1):
        formedAttributes = ""
        if(args):
            formedAttributes += '?_' + \
                ('t' if t else '') + '=' + str(self.__now())
            for label in attributes:
                formedAttributes += '&' + \
                    str(label) + '=' + str(attributes[label])
        outUrl = 'http://' + \
            join(self.ip, address).strip('/') + formedAttributes

        return(outUrl)

    # save session cookie in a json format (file path in self.sessionFile)
    def save(self):
        self.__dep("Saving session")
        f = open(self.sessionFile, 'w+')
        json.dump(requests.utils.dict_from_cookiejar(
            self.networkSession.cookies), f)

    # update current headers
    def __updateHeaders(self):
        self.networkSession.headers.update(self.headers)

    # create the session in self.networkSession and set headers
    def connect(self):
        self.__dep("Created a new session object")
        self.networkSession = requests.Session()
        # set headers
        self.networkSession.headers.update(self.headers)

    # load cookies from json files if it works
    def load(self):
        self.__dep("Loading cookie")
        try:
            with open(self.sessionFile, 'r') as f:
                cookies = requests.utils.cookiejar_from_dict(json.load(f))
                self.networkSession.cookies.update(cookies)
                self.__dep("ok")
            self.headers.update(
                {'X-XSRF-TOKEN': self.networkSession.cookies.get_dict()['XSRF-TOKEN']})
            self.__updateHeaders()
        except FileNotFoundError:
            self.__dep("failed, file not FileNotFoundError")
        except json.decoder.JSONDecodeError:
            self.__dep("failed, json malformed")

    # check if is logged
    def isLogged(self):
        self.__dep("Checking if logged")
        # command 4 check login status
        url = self.__urlFormer(
            'status.cgi', {'cmd': '4', 'nvget': 'login_confirm'})
        response = self.networkSession.get(url)
        self.__dep("Asking for " + url)
        self.__dep("Recivied code: " + str(response.status_code))
        self.__dep("Recivied data: " + response.text)
        if response.status_code != 200:
            raise ConnectionError(
                "Error in connection, response code is %s" % (response.status_code))

        # decoding response
        decodedResponse = json.loads(response.text)
        # true if logged
        return(int(decodedResponse['login_confirm']['login_status']))

    # perform a login: is dummy login, so don't use this function, use insthead
    # smartLogin that log only if not logged (or you will be banned from fastgate
    # until a reboot is performed)
    def login(self):
        # ask index (simulate browser)
        url = self.__urlFormer('index.html', {}, args=0)
        response = self.networkSession.get(url)
        self.__dep("Asking for " + url)
        self.__dep("Recivied code: " + str(response.status_code))
        self.__dep("Recivied data: " + response.text)
        if response.status_code != 200:
            raise ConnectionError(
                "Error in connection, response code is %s" % (response.status_code))

        url = self.__urlFormer('views/modals/modal_errors.html', {}, args=0)
        response = self.networkSession.get(url)
        self.__dep("Asking for " + url)
        self.__dep("Recivied code: " + str(response.status_code))
        self.__dep("Recivied data: " + response.text)
        if response.status_code != 200:
            raise ConnectionError(
                "Error in connection, response code is %s" % (response.status_code))

        # dummy request simulating broser
        self.isLogged()

        # command 1, not clear what it does but performed before login
        url = self.__urlFormer(
            'status.cgi', {'cmd': '1', 'nvget': 'login_confirm'})
        response = self.networkSession.get(url)
        self.__dep("Asking for " + url)
        self.__dep("Recivied code: " + str(response.status_code))
        self.__dep("Recivied data: " + response.text)
        if response.status_code != 200:
            raise ConnectionError(
                "Error in connection, response code is %s" % (response.status_code))

        # simulate browser downloading login form
        url = self.__urlFormer('views/login.html', {}, 1)
        response = self.networkSession.get(url)
        self.__dep("Asking for " + url)
        self.__dep("Recivied code: " + str(response.status_code))
        self.__dep("Recivied data: " + response.text)
        if response.status_code != 200:
            raise ConnectionError(
                "Error in connection, response code is %s" % (response.status_code))

        # command 3, perform login!!
        url = self.__urlFormer('status.cgi', {
            'cmd': '3',
            'nvget': 'login_confirm',
            'password': quote(self.password),
            'remember_me': '1',
            'username': quote(self.username)
        })
        response = self.networkSession.get(url)
        self.__dep("Asking for " + url)
        self.__dep("Recivied code: " + str(response.status_code))
        self.__dep("Recivied data: " + response.text)
        if response.status_code != 200:
            raise ConnectionError(
                "Error in connection, response code is %s" % (response.status_code))

        # return of correctly logged
        if (int(json.loads(response.text)['login_confirm']['check_user']) == 1 and int(json.loads(response.text)['login_confirm']['check_pwd']) == 1):
            # update headers to attach X-XSRF-TOKEN and authenticate
            self.headers.update(
                {'X-XSRF-TOKEN': self.networkSession.cookies.get_dict()['XSRF-TOKEN']})
            self.__updateHeaders()
            self.__dep("Updating headers")
            self.__dep(self.headers)
            return True
        else:
            return False

    # perform a login if alredy not logged, if logged do nothing
    def smartLogin(self):
        if self.isLogged():
            self.__dep("Already logged")
            return True
        else:
            self.__dep("Not logged, perform a login")
            # login
            self.login()
            if self.isLogged():
                return True
            else:
                return False

    # perform a logout
    def logout(self):
        url = self.__urlFormer(
            'status.cgi', {'cmd': '5', 'nvget': 'login_confirm'})
        response = self.networkSession.get(url)
        self.__dep("Asking for " + url)
        self.__dep("Recivied code: " + str(response.status_code))
        self.__dep("Recivied data: " + response.text)
        if response.status_code != 200:
            return(False)
        if json.loads(response.text)['login_confirm']['login_confirm'] == 'end':
            return True
        else:
            return False

    # get systeminfo
    def info(self):
        url = self.__urlFormer('status.cgi', {'nvget': 'sysinfo'})
        response = self.networkSession.get(url)
        self.__dep("Asking for " + url)
        self.__dep("Recivied code: " + str(response.status_code))
        self.__dep("Recivied data: " + response.text)
        if response.status_code != 200:
            return(False)
        return(json.loads(response.text)['sysinfo'])

    # perform a reboot of the fastgate
    def reboot(self):
        self.info()
        url = self.__urlFormer(
            'status.cgi', {'act': 'nvset', 'service': 'reset'})
        response = self.networkSession.get(url)
        self.__dep("Asking for " + url)
        self.__dep("Recivied code: " + str(response.status_code))
        self.__dep("Recivied data: " + response.text)

        # if response is 403 there was a wrong token and I should get new one
        if response.status_code == 403:
            if self.retry:
                self.__dep("Error 403, retry")
                self.retry = 0
                self.headers.update({'X-XSRF-TOKEN': ''})
                self.__updateHeaders()
                self.connect()
                self.smartLogin()
                result = self.reboot()
                return(result)
            else:
                raise ConnectionError(
                    "Error in connection, response code is %s" % (response.status_code))

        elif response.status_code != 200:
            raise ConnectionError(
                "Error in connection, response code is %s" % (response.status_code))
        if(json.loads(response.text)['nvset'] == 'ok'):
            return True
        else:
            return False
