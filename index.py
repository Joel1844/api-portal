from dotenv import load_dotenv
from os import getenv

load_dotenv()

if __name__ == '__main__':
    import uvicorn
    HOST = getenv('HOST')
    PORT = getenv('PORT')
    uvicorn.run('app:app', reload=True, host=HOST, port=int(PORT))