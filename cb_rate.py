import aiohttp


async def get_current_usd() -> float:
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.json(content_type="application/javascript")
            current_usd = response["Valute"]["USD"]["Value"]
            return current_usd
