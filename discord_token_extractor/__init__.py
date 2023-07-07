from pyotp import TOTP
from binascii import Error
from playwright.sync_api import sync_playwright, TimeoutError as SyncPWTimeoutError
from playwright.async_api import async_playwright, TimeoutError as AsyncPWTimeoutError

class Extractor:
    def __init__(self, email: str, password: str, totp_secret: str = None):
        self.email = email
        self.password = password
        self.totp_secret = totp_secret

    def sync_extract_token(self):
        while True:
            try:
                with sync_playwright() as pw:
                    browser = pw.firefox.launch()
                    page = browser.new_page()

                    page.goto("https://discord.com/login")
                    page.locator("//*[@id='app-mount']/div[2]/div[1]/div[1]/div/div/div/div/form").wait_for()
                    page.locator("//html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/input").fill(self.email)
                    page.locator("//html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/div[2]/div/input").fill(self.password)
                    page.locator("//*[@id='app-mount']/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]").click()

                    try:
                        page.locator("//*[@id='app-mount']/div[2]/div[1]/div[1]/div/div/div/form").wait_for()

                    except SyncPWTimeoutError:
                        try:
                            page.locator("//*[@id='app-mount']/div[2]/div[1]/div[4]/div[2]/div/div/div/div[1]/div[4]").wait_for()

                        except SyncPWTimeoutError:
                            raise InvalidCredentialsError("The credentials you provided are invalid")

                        else:
                            raise CaptchaError("A captcha was raised, this is most likely due to the credentials being invalid or you spamming the Discord API")

                    else:
                        if self.totp_secret:
                            try:
                                page.query_selector("//html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/form/div[2]/div[2]/div/div/input").fill(TOTP(self.totp_secret).now())

                            except Error:
                                raise InvalidTOTPSecret("The TOTP secret you provided is invalid, maybe format it without spaces.")

                            page.locator("//*[@id='app-mount']/div[2]/div[1]/div[1]/div/div/div/form/div[2]/div[2]/button[1]").click()

                        else:
                            raise NoTOTPSecretProvidedError("Discord is asking for a 2fa OTP and you didn't provide a TOTP secret, please provide one.")

                        try:
                            page.locator("//*[@id='online-tab']/div[1]/div/input").wait_for()

                        except SyncPWTimeoutError:
                            raise InvalidTOTPSecret("The TOTP secret you provided is not that of your Discord account'.")

                        token = page.evaluate("() => { return (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken(); }")

                        browser.close()

                        return token

            except AsyncPWTimeoutError:
                continue

    async def async_extract_token(self):
        while True:
            try:
                with async_playwright() as pw:
                    browser = await pw.firefox.launch()
                    page = await browser.new_page()

                    await page.goto("https://discord.com/login")
                    await page.locator("//*[@id='app-mount']/div[2]/div[1]/div[1]/div/div/div/div/form").wait_for()
                    await (await page.query_selector("[aria-labelledby=':r0:']")).fill(self.email)
                    await (await page.query_selector("[aria-labelledby=':r1:']")).fill(self.password)
                    await page.locator("//*[@id='app-mount']/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]").click()

                    try:
                        await page.locator("//*[@id='app-mount']/div[2]/div[1]/div[1]/div/div/div/form").wait_for()

                    except AsyncPWTimeoutError:
                        try:
                            await page.locator("//*[@id='app-mount']/div[2]/div[1]/div[4]/div[2]/div/div/div/div[1]/div[4]").wait_for()

                        except AsyncPWTimeoutError:
                            raise InvalidCredentialsError("The credentials you provided are invalid")

                        else:
                            raise CaptchaError("A captcha was raised, this is most likely due to the credentials being invalid or you spamming the Discord API")

                    else:
                        if self.totp_secret:
                            try:
                                await (await page.query_selector("[aria-labelledby=':r2:']")).fill(TOTP(self.totp_secret).now())

                            except Error:
                                raise InvalidTOTPSecret("The TOTP secret you provided is invalid, maybe format it without spaces.")

                            await page.locator("//*[@id='app-mount']/div[2]/div[1]/div[1]/div/div/div/form/div[2]/div[2]/button[1]").click()

                        else:
                            raise NoTOTPSecretProvidedError("Discord is asking for a 2fa OTP and you didn't provide a TOTP secret, please provide one.")

                        try:
                            await page.locator("//*[@id='app-mount']/div[2]/div[1]/div[1]/div/div[2]/div/div/nav/ul").wait_for()

                        except AsyncPWTimeoutError:
                            raise InvalidTOTPSecret("The TOTP secret you provided is not that of your Discord account'.")

                        token = await page.evaluate("() => { return (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken(); }")

                        await browser.close()

                        return token

            except SyncPWTimeoutError:
                continue

class CaptchaError(Exception):
    pass

class InvalidTOTPSecret(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class NoTOTPSecretProvidedError(Exception):
    pass
