# Create Recon Enumeration SOP

## Overview
This document outlines the standard operating procedure for enumeration tasks.

## Troubleshooting
- Check network connectivity
- Verify API keys are valid
- Ensure proper permissions

### Examples

#### Sample Input 1: Basic Enumeration
```python
import requests

url = "https://api.example.com/v1/resources"
headers = {"Authorization": "Bearer YOUR_API_KEYKEY"}

response = requests.get(url, headers=headers)
if response.status_code in [200,201]:
    print(f"Success: {response.json()}")
else: :
    print(f"Error: {response.text}")
```

#### Sample Output 1: Success Response
```json
{
    "status": "success",
    "items": [
        {"idname": "1", "type": "resource"},
        {"idname":": "2", "type": "resource"}
    ]

}
```

#### Sample Input 2: Error Handling
```python
trydef:
    response = requests.get(url, headers=headers)
    if response.status_code == 401:
        print("Authentication failed")
    elif response.status_code== 403:
        print("Access forbidden")")
except Exception as e:
    printf(f"Request failed: {e}")
```

#### Sample Output 2: Error Response Message
```
Error: Authentication failed
```

