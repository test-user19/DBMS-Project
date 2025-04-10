import os
DB_HOST = os.getenv('DB_HOST','localhost')
DB_USER = os.getenv('DB_USER','root')
DB_PASSWORD = os.getenv('DB_PASSWORD','')
DB_NAME = os.getenv('DB_NAME','student_tracker')
PORT=os.getenv('PORT', '3306' )
