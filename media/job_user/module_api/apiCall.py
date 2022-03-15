import pycurl
import json
from io import StringIO

curl = pycurl.Curl()

## 서버 아이피 경로
curl.setopt(pycurl.URL, 'http://192.168.1.222:50051/predict')
curl.setopt(pycurl.HTTPHEADER, ['Accept: application/json',
                                'Content-Type: application/json'])
curl.setopt(pycurl.POST, 1)

# If you want to set a total timeout, say, 3 seconds
curl.setopt(pycurl.TIMEOUT_MS, 3000)

## depending on whether you want to print details on stdout, uncomment either
# curl.setopt(pycurl.VERBOSE, 1) # to print entire request flow
## or
# curl.setopt(pycurl.WRITEFUNCTION, lambda x: None) # to keep stdout clean

# preparing body the way pycurl.READDATA wants it
# NOTE: you may reuse curl object setup at this point
# if sending POST repeatedly to the url. It will reuse
# the connection.

##### geon 추가 #####
##### content는 smiles 내용 입력
##### jobID 추가 필요!!!!!!!!!!!!!!!!!!!!!!!!!!
##### 보낼때 jobID 생성!!!!!!

body_as_dict = {"content": "OC(c1ccccc1)(c2ccccc2)C4CCN(CCCC(O)c3ccc(cc3)C(C)(C)C)CC4"}
body_as_json_string = json.dumps(body_as_dict) # dict to json
body_as_file_object = StringIO(body_as_json_string)

# prepare and send. See also: pycurl.READFUNCTION to pass function instead
curl.setopt(pycurl.READDATA, body_as_file_object)
curl.setopt(pycurl.POSTFIELDSIZE, len(body_as_json_string))
curl.perform()

# you may want to check HTTP response code, e.g.
status_code = curl.getinfo(pycurl.RESPONSE_CODE)
if status_code != 200:
    print("Aww Snap :( Server returned HTTP status code {}".format(status_code))

# don't forget to release connection when finished
curl.close()
