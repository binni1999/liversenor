from fastapi import FastAPI

app = FastAPI() 

@app.get("/")
async def root():
    return "Hello welcome to binni blogs!"

@app.get("/hello/{name}")
async def hello(name):
    return {"message":f"Hello {name}"}



indian_places = {
    'delhi':['Red Fort','Qutub Minar', 'India Gate'],
    'mumbai':['Gateway of india','Marine Drive','Elephanta Caves'],
    'jaipur':['Hawa Mahal','Amber Fort','City Palace'],
    'varanasi':['Kashi Vishwanath','Ghats of Banaras'],
    'goa':["Baga Beach",'Calanguate Beach','Dudhsagar Falls'],
}

@app.get("/get_items/{city}")
async def get_items(city): 
    return indian_places.get(city)
