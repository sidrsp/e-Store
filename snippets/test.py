import base64
from datetime import datetime, timedelta
import os



def get_token(expires_in=3600):
    now = datetime.utcnow()
    print(f"utcnow : {now}")

    # now = datetime.time()
    # print(f"time : {now}")
    #
    # now = datetime.timestamp()
    # print(f"timestamp : {now}")
    #
    # now = datetime.timetuple()
    # print(f"timetuple : {now}")
    #
    # now = datetime.timetz()
    # print(f"timetz : {now}")


    # for i in range(10):
    #     token = base64.b64encode(os.urandom(24)).decode('utf-8')
    #     print(f"token : {token}")


    # blah = base64.b64encode(os.urandom(24))
    blah = os.urandom(24)
    print(f"blah : {blah}")
    # print(f"blah : {blah.decode('UTF-8')}")



    token_expiration = now + timedelta(seconds=expires_in)
    print(f"token expiration : {token_expiration}")


if __name__ == '__main__':
    get_token()