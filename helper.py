import requests
from subprocess import call
import re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

def fetchSite(url):
    print('Fetching site...')

    try:
        result = requests.get(url, headers=HEADERS) 
        result.raise_for_status()
        return result
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.ConnectionError as err:
        raise SystemExit(err)
    except requests.exceptions.Timeout as err:
        raise SystemExit(err)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

def FTP(url,file,directory):
    directory = re.sub('[^A-Za-z0-9_\.\- ]+','',directory)
    file = re.sub('[^A-Za-z0-9_\.\- ]+','',file)
    call(['mkdir','-p', directory])
    call(['wget', '-c', url, '-O', directory + '/' + file])
