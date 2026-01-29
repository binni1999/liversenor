from fastapi import FastAPI
app = FastAPI() 


@app.get("/hello/{name}")
async def root(name): 
    return f"Hello world,my name is {name}"