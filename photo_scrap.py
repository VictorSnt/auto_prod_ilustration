from Configuration.DbConection.DbConnect import DbConnection
from queries import products_query, get_all_groups_query

from playwright.async_api import async_playwright
from dotenv import load_dotenv
from pathlib import Path
import asyncio
import os


async def download_prod_img(downloads_folder: str, product_name: str, prod_id: str):
    async with async_playwright() as p:
        browser = await p.firefox.launch_persistent_context(
            './configuration/profile',
            headless=False
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


if __name__ == '__main__':

    async def init_async():

        downloads_folder: Path = Path(os.environ.get('IMG_FOLDER', ''))

        downloaded_photos: dict[str:Path] = {
            x.stem: x for x in downloads_folder.iterdir()
                if downloads_folder.exists()
            }
        
        db_conn = DbConnection(os.environ.get('HOST', False), 
                            os.environ.get('PORT', False), 
                            os.environ.get('DBNAME', False), 
                            os.environ.get('USER', False), 
                            os.environ.get('PASSWD', False))
        
        if not db_conn.connect(): raise db_conn.error
        
        groups_response = db_conn.sqlquery(query=get_all_groups_query)
        
        if not groups_response: input(db_conn.error)
        
        active_groups = [group_row for group_row in groups_response 
                        if not any(char in group_row.get('nmgrupo', '') for char in ['@', '*'])]
        

        excluded_groups = ["N5D000001L", "N5D000000F", "N5D000000S", 
                           "N5D0000012", "N5D0000005", "N5D000000H"]
        active_groups = [group_row for group_row in active_groups 
                         if not group_row['idgrupo'] in excluded_groups]
        
        for group in active_groups:
            prod_query = products_query.format(group['idgrupo'])
            prods_response = db_conn.sqlquery(query=prod_query) # this will be unique for each db structure, this one is a example
            if not prods_response: continue
            for res in prods_response:
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