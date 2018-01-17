import os

api_secret = 'n1nbbz79akqq4q5d4zykol309p75ms9w'
api_key = '6377ppayo82pmi8f'
userid = 'YZ0647'
mysqluser = 'root'
mysqlpassword = '#BLUEdogm131139#'


def getApiKey():
    return api_key


def getApiSecret():
    return api_secret


def getUserID():
    return userid


def getMysqlUser():
    return mysqluser


def getMysqlPassword():
    return mysqlpassword


def getRootPath():
    cwd = os.getcwd()
    root_path_index = cwd.find('AlgoTrading')
    root_path = cwd[0:root_path_index]
    return root_path
