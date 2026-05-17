import requests

# Create a session to persist cookies/login state
session = requests.Session()

# 1. Log in
login_url = "http://127.0.0.1:5000/login"
login_data = {
    "username": "khsophea20@gmail.com",
    "password": "@Sp18052005"
}
print("Logging in...")
r_login = session.post(login_url, json=login_data)
print(f"Login response status: {r_login.status_code}")
print(f"Login response body: {r_login.text}")

# 2. Try to generate email
gen_url = "http://127.0.0.1:5000/generate_email"
gen_data = {
    "domain": "wshu.net"
}
print("\nGenerating email...")
r_gen = session.post(gen_url, json=gen_data)
print(f"Generate response status: {r_gen.status_code}")
print(f"Generate response body: {r_gen.text}")
