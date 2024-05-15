import requests

res = requests.post("http://127.0.0.1:3000/api/main/3",  {"name": "Go", "videos": 10},)# отправляем гет запрос  сервер локальный
print(res.json())
