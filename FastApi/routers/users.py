from fastapi import APIRouter,HTTPException
from pydantic import BaseModel


router = APIRouter(tags=["users"])

class User(BaseModel):
    id:int
    name:str
    surname:str
    url:str
    age:int


users_list = [
    User(id=1,name="Eulalio",surname="Cruz",url="https://eulalio.com",age=32),
    User(id=2,name="Yolanda",surname="Cruz",url="https://yolanda.com",age=30),
    User(id=3,name="Maricela",surname="Cruz",url="https://maricela.com",age=28)
]

# @router.get("/usersjson")
# async def root():
#     return [
#         {"name":"Eulalio","surname":"Cruz","url":"https://eulalio.com","age":31},
#         {"name":"Yolanda","surname":"Cruz","url":"https://yolanda.com","age":30},
#         {"name":"Maricela","surname":"Cruz","url":"https://maricela.com","age":28}
#     ]

@router.get("/users")
async def users():
    return users_list


@router.get("/user/{id}")
async def user(id:int):
    return search_user(id)
    

@router.get("/user/")
async def user(id:int):
    return search_user(id)


@router.post("/user/",response_model=User,status_code=201)
async def user(user:User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204,detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user


@router.put("/user/")
async def user(user:User):
    found = False

    for index, save_user in enumerate(users_list):
        if save_user.id == user.id:
            users_list[index] = user
            found = True
            
    
    if not found:
        return {"Error":"Usuario atualizar, no se ha encontrado"}
    else:
        return user


@router.delete("/user/{id}")
async def user(id:int):
    found = False

    for index, save_user in enumerate(users_list):
        if save_user.id == id:
            users_list[index] = user
            found = True

    if not found:
        return {"Error":"No se ha eliminado el usuario"}
    
    return {"message":"Usuario eliminado correctamente"}
    

def search_user(id:int):
    users = filter(lambda user: user.id == id , users_list)
    try:
        return list(users)[0]
    except:
        return {"Error":"No se encontro el usuario"}