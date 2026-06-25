#new social media project 
From fastapi import FastAPI
app=FastAPI()
@app.get("/")
async def get_all_posts():
