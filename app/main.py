from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import requests
from .config import settings

app = FastAPI()

@app.get("/preview/{file_path:path}")
async def get_preview(file_path: str):
    # Encode the path for the request to Windows server
    encoded_path = requests.utils.quote(file_path, safe='')
    windows_server_url = f"http://{settings.WINDOWS_SERVER_IP}:{settings.WINDOWS_SERVER_PORT}/preview/{encoded_path}"

    try:
        # Make a GET request to the Windows server to retrieve the file
        response = requests.get(windows_server_url, stream=True)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx

        # Use StreamingResponse to send the file content to the client
        return StreamingResponse(response.iter_content(chunk_size=1024), media_type=response.headers['Content-Type'])
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving file: {str(e)}")
