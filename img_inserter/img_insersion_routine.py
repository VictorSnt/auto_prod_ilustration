from Configuration.DbConection.DbConnect import DbConnection
from Configuration.DbConection.queries import insert_query, get_product_foto
from dotenv import load_dotenv
from psycopg2 import Binary
from pathlib import Path
from PIL import Image
import io
import os


def insert_foto_in_database(image_path: Path, db_conn: DbConnection):
    
    load_dotenv()
    
    imagem = Image.open(image_path)
    buffer = io.BytesIO()

    try:
        
        imagem.save(buffer, format='JPEG')

    except Exception:

        rgb_image = imagem.convert('RGB')
        rgb_image.save(buffer, format='JPEG')
        
    dados_binarios = buffer.getvalue()
    
    query = insert_query.format(
            image_path.stem, image_path.stem, image_path.name,
            Binary(dados_binarios), Binary(dados_binarios)
        ) 
    
    db_conn.sqlquery(query=query, commit=True)
    if db_conn.error:  raise db_conn.error
    

db_conn = DbConnection(
    host=os.environ.get('HOST', False), 
    port=os.environ.get('PORT', False), 
    dbname=os.environ.get('DBNAME', False), 
    user=os.environ.get('USER', False), 
    password=os.environ.get('PASSWD', False)
    )

if not db_conn.connect(): raise db_conn.error

downloads_folder = Path(os.environ.get('IMG_FOLDER', ''))
imagem_path = [file for file in Path(downloads_folder).iterdir() if downloads_folder.exists()]
if not imagem_path: raise ValueError("o array image_path esta vazio")

for file in imagem_path:

    response = db_conn.sqlquery(get_product_foto.format(file.stem))

    if not response:
        insert_foto_in_database(file, db_conn)
        
db_conn.conn.commit()
