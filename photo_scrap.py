from playwright.async_api import async_playwright
from Configuration.DbConection.DbConnect import DbConnection
from pathlib import Path
import Configuration.config as run_conf
import asyncio
from queries import products_query

async def download_prod_img(downloads_folder: str, product_name: str, prod_id: str):
    async with async_playwright() as p:
        browser = await p.firefox.launch_persistent_context(
            './configuration/profile',
            headless=True
        )
        page = await browser.new_page()
        await page.goto('https://www.google.com.br/imghp?hl=pt-BR&authuser=0&ogbl')
        await page.wait_for_selector('#APjFqb')
        search_input = page.locator('#APjFqb')
        await search_input.type(product_name)
        await page.wait_for_selector('[jsname="Tg7LZd"]')
        await page.click('[jsname="Tg7LZd"]')
        await page.wait_for_selector('[jsname="Q4LuWd"]')
        img_element = page.locator('[jsname="Q4LuWd"]').first
        screenshot_data = await img_element.screenshot()
        with open(f'{downloads_folder}/{prod_id}.png', 'wb') as f:
            f.write(screenshot_data)
        
        

    # Ao sair do bloco `async with`, o contexto do navegador será fechado automaticamente


if __name__ == '__main__':
    async def init_async():
        downloads_folder ='./produtos'
        downloaded_photos = {x.stem: x for x in Path(downloads_folder).iterdir()}
        conf = run_conf.load_config()
        if not conf:
            print('Error loading config')

        db_conn = DbConnection(conf['HOST'], 
                            conf['PORT'], 
                            conf['DBNAME'], 
                            conf['USER'], 
                            conf['PASSWD'])
        db_conn.connect()
        response = db_conn.sqlquery(query=products_query) # this will be unique for each db structure, this one is a example
        if not response: input(db_conn.error)
        for res in response:
            prod_name: str = res['dsdetalhe']
            prod_id: str = res['iddetalhe']
            
            if not downloaded_photos.get(prod_id, False):
                try:
                    await download_prod_img(downloads_folder, prod_name, prod_id)
                except Exception as e:
                    print(e)
                    continue
        print('done')
    asyncio.run(init_async())