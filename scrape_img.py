import time, base64, datetime
import asyncio
from pyppeteer import launch

async def puppeteer_get_data(mp_filter=None):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})

    await page.goto("https://beammp.com/servers")
    await asyncio.sleep(5)

    if not mp_filter==None:
        await page.waitForSelector('#dataTable_filter > label > input')
        await page.type('#dataTable_filter > label > input', mp_filter)
        time.sleep(1)

    html_s = await page.content()
    print(html)

    await browser.close()

asyncio.get_event_loop().run_until_complete(puppeteer_get_data("cops n robber"))