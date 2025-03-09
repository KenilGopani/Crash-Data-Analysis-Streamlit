import base64

with open("./../bigquery-key.json", "r") as f:
    key_content = f.read()
    encoded_key = base64.b64encode(key_content.encode()).decode()

print(encoded_key)

