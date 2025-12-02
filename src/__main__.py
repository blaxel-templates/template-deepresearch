import uvicorn
from blaxel import env

port = env["PORT"]
host = env["HOST"]

if __name__ == "__main__":
    uvicorn.run("src.main:app", host=host, port=int(port), reload=False)