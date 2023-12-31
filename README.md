# Discord Token Extractor
## About
This is a library to get a Discord user token from an email, password and optionally the TOTP secret. This is being done with [Playwright](https://playwright.dev/python/) (a browser automation framework).

## Key Features
- Exception catching
- 2fa support (only for OTP)

## Installation
To install Discord Token Extractor run:
```bash
pip install git+https://github.com/BlueSchnabeltier/discord-token-extractor.git
```

## Examples
### Basic Example
```python
from asyncio import run
from discord_token_extractor import Extractor

email = "example@example.com"  # Replace with your email
password = "Password123!"  # Replace with your password
totp_secret = "1abc2defgh3ij4kl"  # Replace with your TOTP secret, if your account doesn't have 2fa you don't have to specify it as a parameter

extractor = Extractor(email, password, totp_secret)  # Defines an extractor

# SYNC VERSION
def main(extractor: Extractor):
    token = extractor.sync_extract_token()  # Extracts the token

    print(token)

main(extractor)

# ASYNC VERSION
async def main(extractor: Extractor):
    token = await extractor.async_extract_token()  # Extracts the token

    print(token)

run(main(extractor))
```
