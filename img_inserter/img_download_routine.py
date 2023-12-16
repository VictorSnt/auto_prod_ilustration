from Configuration.DbConection.DbConnect import DbConnection
from Configuration.DbConection.queries import products_query, get_all_groups_query
from img_inserter.playwright.photo_scrap import download_prod_img

from dotenv import load_dotenv
from pathlib import Path
import asyncio
import os


async def init_async():

        load_dotenv()
        downloads_folder: Path = Path(os.environ.get('IMG_FOLDER', ''))
        downloaded_photos: dict[str:Path] = {
            x.stem: x for x in downloads_folder.iterdir()
                if downloads_folder.exists()
            }
        
        db_conn = DbConnection(
            host=os.environ.get('HOST', False), 
            port=os.environ.get('PORT', False), 
            dbname=os.environ.get('DBNAME', False), 
            user=os.environ.get('USER', False), 
            password=os.environ.get('PASSWD', False)
            )
        
        if not db_conn.connect(): raise db_conn.error
        
        groups_response = db_conn.sqlquery(query=get_all_groups_query)
        
        if not groups_response: raise db_conn.error
        
        active_groups = [
            group_row for group_row in groups_response 
                if not any(char in group_row.get('nmgrupo', '') for char in ['@', '*'])
            ]
        
        for group in active_groups:
            
            prod_query = products_query.format(group['idgrupo'])
            prods_response = db_conn.sqlquery(query=prod_query) 

            if not prods_response: continue
            
            for res in prods_response:

                prod_name: str = res['dsdetalhe']
                prod_id: str = res['iddetalhe']
                
                if not downloaded_photos.get(prod_id, False):
                    try:
                        await download_prod_img(downloads_folder, prod_name, prod_id)
                    except TimeoutError as e:
                        print(e)
                        continue
        

if __name__ == '__main__':

    
    asyncio.run(init_async())