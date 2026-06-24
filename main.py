from fastapi import FastAPI 
from route.init import router 

app = FastAPI()

app.include_router(router)