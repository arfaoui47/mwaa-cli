from typing import Optional

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/run_command")
def run_cmd():
    return {"Hello": "World"} 



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)