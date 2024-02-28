import time, datetime
import asyncio, requests, json
from pyppeteer import launch
from bs4 import BeautifulSoup


def ping_general_change_f(formatted_json_final):
    with open("config.json","r") as config_f:
        config_c = json.load(config_f)

    config_c_reworked = []
    for config_now in config_c:
        data = {}
        data["embeds"] = []
        embed = {}
        embed["color"] = config_now["color"]
        embed["title"] = "CnR Server List"
        embed["timestamp"] = datetime.datetime.now().isoformat()
        embed["description"] = ""
        for server_now in formatted_json_final:
            embed["description"] = embed["description"] + f'{str(server_now["server_name"])}\n> {str(server_now["server_map"])}  [{str(server_now["player_count"])}]\n\n'
        embed["footer"] = {
            "text": "BeamMP Server Stats CnR",
            "icon_url": "https://asdatindustries.com/static/cnr_logo.PNG"
        }
        data["embeds"].append(embed)

        if not config_now["temp_var_overwrite"] == "":
            delete_r = requests.delete(config_now["webhook_url"]+"/messages/"+config_now["temp_var_overwrite"], headers={"Content-Type": "application/json"})
            config_now["temp_var_overwrite"] = ""

        disc_webh_result = requests.post(config_now["webhook_url"], data=json.dumps(data),params={"wait":True}, headers={"Content-Type": "application/json"})
        resp_json = json.loads(disc_webh_result.text)
        config_now["temp_var_overwrite"] = resp_json["id"]

        config_c_reworked.append(config_now)

        print("[PING] " + str(config_now["info"]))

    with open("config.json","w") as config_f:
        json.dump(config_c_reworked,config_f)


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
    soup = BeautifulSoup(html_s, 'html.parser')

    formatted_json_final = []

    all_table_lines = soup.find("tbody", {"id": "Servers-List"}).find_all("tr")
    for table_entry_now in all_table_lines:
        table_entry_part_list = table_entry_now.find_all("td")
        location = table_entry_part_list[0].text
        server_name = table_entry_part_list[1].text

        server_name = server_name.split("|")[0] #extremely long fuckin server name xD
        server_name = server_name.replace("☢Cops n Robbers☢ Dedicated","CnR")

        server_map = table_entry_part_list[2].text
        player_count = table_entry_part_list[3].text

        if not "Xevnet.Events" in server_name: #some other server named Cops n Robbers
            formatted_json_final.append({"location":location,"server_name":server_name,"server_map":server_map,"player_count":player_count})

    ping_general_change_f(formatted_json_final)

    await browser.close()

asyncio.get_event_loop().run_until_complete(puppeteer_get_data("cops n robber"))