import requests

with open(r'C:\Users\User\Documents\testi.sqlite3', 'rb') as file:
    files = {'file': file}
    response = requests.post('http://127.0.0.1:8080/upload/', files=files)

# Check the response status code
if response.status_code == 201:
    print("POST request was successful.")
    print("Response:", response.json())
else:
    print("POST request failed with status code:", response.status_code)
