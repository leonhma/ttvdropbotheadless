# pylama:ignore=E501

from http.cookiejar import LWPCookieJar
from requests import Session


cj = LWPCookieJar(filename='./cookies.txt')
sess = Session()
sess.cookies = cj

try:
    cj.load()
except Exception:
    pass

r = sess.post(
    'https://www.twitch.tv/',
    json={"username": "leonhma", "password": "1243?abDc",
          "client_id": "oooo78kx3ncx6brgo4mv6wki5h1ko",
          "undelete_user": False})

print(cj)
print(f'{r.text = }\n{r.status_code = }\n{r.headers = }')

cj.save()
