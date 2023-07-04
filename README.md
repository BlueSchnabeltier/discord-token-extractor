# Discord Token Extractor
## About
This is a library to get a Discord user token from an email, password and optionally the TOTP secret. This is being done with [Vinyzu/Botright](https://github.com/Vinyzu/Botright/) (a [Playwright](https://playwright.dev/python/) fork).

## Features
- Exception catching
- 2fa support (only for OTP)

# Example
Here is a basic example that prints the token to the terminal:
```python
from asyncio import run
from discord_token_extractor import Extractor

email = "example@example.com"  # Replace with your email
password = "Password123!"  # Replace with your password
totp_secret = "1abc2defgh3ij4kl"  # Replace with your TOTP secret, if your account doesn't have 2fa you dont have to specify it as a parameter

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

run(main(extractor))```
