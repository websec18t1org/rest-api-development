import requests

print "[1] Testing /"
headers = {
    'Content-Type': 'application/json',
}

response = requests.get('http://localhost:8080/', headers=headers)
print response.content

print "[2] Testing /users/register"
headers = {
    'Content-Type': 'application/json',
}

data = '{"username": "AzureDiamond",  "password": "hunter2",  "fullname": "Joey Pardella",  "age": 15}'

response = requests.post('http://localhost:8080/users/register', headers=headers, data=data)
print response.content

print "[3] Testing /users/authenticate"
headers = {
    'Content-Type': 'application/json',
}

data = '{"username": "AzureDiamond",  "password": "hunter2"}'

response = requests.post('http://localhost:8080/users/authenticate', headers=headers, data=data)
print response.content

print "[4] Testing /users/expire"
data = response.content
print data
headers = {
    'Content-Type': 'application/json',
}

#data = '{"token": ""5fc077b2-cc5d-40b3-8d6d-ac3395e35d0e}'

response = requests.post('http://localhost:8080/users/expire', headers=headers, data=data)

print response.content

print "[5] Testing /users"
#create new user
headers = {
    'Content-Type': 'application/json',
}

data = '{"username": "audrey123talks","password":"test123","fullname": "Audrey Shida", "age": 14}'

response = requests.post('http://localhost:8080/users/register', headers=headers, data=data)
print response.content

headers = {
    'Content-Type': 'application/json',
}

data = '{"username": "audrey123talks",  "password": "test123"}'

response = requests.post('http://localhost:8080/users/authenticate', headers=headers, data=data)

data = response.content
print data
headers = {
    'Content-Type': 'application/json',
}
response = requests.post('http://localhost:8080/users', headers=headers, data=data)

print response.content

# print "[6] Testing /diary/create"
#
# headers = {
#     'Content-Type': 'application/json',
# }
#
# data = '{"username": "AzureDiamond",  "password": "hunter2"}'
# response = requests.post('http://localhost:8080/users/authenticate', headers=headers, data=data)
#
# data = response.content
# response = requests.post('http://localhost:8080/diary/create', headers=headers, data=data)
#
# print response.content
