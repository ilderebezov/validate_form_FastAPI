import uvicorn
from src.server import app
from src import routes as api_routes


port = 8080

app.include_router(api_routes.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=int(port), reload=False)
