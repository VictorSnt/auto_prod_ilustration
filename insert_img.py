import Configuration.config as run_conf
from Configuration.DbConection.DbConnect import DbConnection
from queries import insert_query
from pathlib import Path
from PIL import Image
from psycopg2 import Binary
import io


def insert_foto_in_database(image_path: Path, db_conn: DbConnection):
    
    imagem = Image.open(image_path)
    buffer = io.BytesIO()
    try:
        imagem.save(buffer, format='JPEG')
    except Exception as e:

        rgb_image = imagem.convert('RGB')
        rgb_image.save(buffer, format='JPEG')
        
    dados_binarios = buffer.getvalue()

    
    query = insert_query.format(
            image_path.stem, image_path.stem, image_path.name,
            Binary(dados_binarios), Binary(dados_binarios)
        ) # this will be unique for each db structure, this one is a example
    db_conn.sqlquery(query=query, commit=True)
    if db_conn.error:  input(db_conn.error)
    

conf = run_conf.load_config()
if not conf:
    print('Error loading config')

db_conn = DbConnection(conf['HOST'], 
                       conf['PORT'], 
                       conf['DBNAME'], 
                       conf['USER'], 
                       conf['PASSWD'])

if not db_conn.connect():
    print(db_conn.error)


imagem_path = [file for file in Path('./produtos').iterdir()]
sliced_path = imagem_path

for file in sliced_path:
    insert_foto_in_database(file, db_conn)
    print('looped')
db_conn.conn.commit()
print('done')