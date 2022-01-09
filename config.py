import os
import socket

ip = "http://localhost:3000"

working_dir = os.path.abspath(__file__).replace('/config.py', '')

test_db_filename = f'{working_dir}/test_db.sqlite'

prod_db = f'{working_dir}/database.sqlite'
