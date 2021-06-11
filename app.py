import uvicorn
from fastapi import FastAPI

from routes.post import router as PostRouter

app = FastAPI()


@app.get('/', tags=['Root'])
async def read_root():
    return {'message': 'Welcome to this face recognition app.'}

app.include_router(PostRouter, tags=['Posts'], prefix='/api')

if __name__ == '__main__':
    uvicorn.run(app, debug=True)
