import requests

# Replace with your actual API key
FACTSET_API_KEY = "<key>"


# API endpoint
url = "https://api.factset.com/content/factset-news/v1/articles"

# Headers
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {FACTSET_API_KEY}"
}

# Parameters (adjust as needed)
params = {
    "limit": 5,
    "offset": 0
}

# Make the request
response = requests.get(url, headers=headers, params=params)

# Check the response
if response.status_code == 200:
    print("Success!")
    print(response.json())
elif response.status_code == 403:
    print("Forbidden: You don't have permission to access this resource.")
elif response.status_code == 404:
    print("Not Found: The requested resource could not be found.")
else:
    print(f"Error {response.status_code}: {response.text}")
