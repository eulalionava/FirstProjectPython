from fastapi import FastAPI
from routers import products,users,jwt_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)



app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/")
async def root():
    return "Hola mundo"

@app.get("/url")
async def url():
    return {"url":"https://enviedinero.com"}