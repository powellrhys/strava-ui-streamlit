from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def configure_server():
    '''
    Input: None
    Output: Fast API server
    Function to configure FAST API server
    '''
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
