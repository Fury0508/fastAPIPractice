from fastapi import Header, HTTPException

API_KEY = "123"

def verify_api_key(x_api_key: str = Header()):
    """ Verify the API key from the request header"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail = "Invalid API key")
    return x_api_key