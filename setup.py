from setuptools import setup

setup(
  name="discord-token-extractor",
  version="1.0",
  description="A library to get a Discord user token from an email, password and optionally the TOTP secret (for 2fa)",
  author="BlueSchnabeltier",
  author_email="finn.ueschner@icloud.com",
  url="https://github.com/BlueSchnabeltier/discord-token-extractor",
  packages=["discord_token_extractor"],
  install_requires=["playwright-driver-autoinstall@git+https://github.com/BlueSchnabeltier/playwright-driver-autoinstall.git"]
)
