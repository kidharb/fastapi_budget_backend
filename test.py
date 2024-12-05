import uvicorn
from datetime import datetime
from fastapi import FastAPI
import pdb

app = FastAPI()

@app.get('/')
def root():
    now = datetime.now()
    pdb.set_trace()
    return { "now": now }

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
 
