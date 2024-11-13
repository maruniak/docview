from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import StreamingResponse, HTMLResponse
import requests
from docx import Document
import openpyxl
import io
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. Replace with specific origins if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods.
    allow_headers=["*"],  # Allow all headers.
)

@app.api_route("/preview/{file_path:path}", methods=["GET", "POST"])
async def get_preview(file_path: str, x_access_token: str = Header(None)):
    # Check if authentication is enabled
    if settings.AUTHENTICATION_ENABLED:
        # If enabled, validate the token
        if x_access_token != settings.ACCESS_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

    # Encode the path for the request to the Windows server
    encoded_path = requests.utils.quote(file_path, safe='')
    windows_server_url = f"http://{settings.WINDOWS_SERVER_IP}:{settings.WINDOWS_SERVER_PORT}/preview/{encoded_path}"

    try:
        # Make a GET request to the Windows server to retrieve the file
        response = requests.get(windows_server_url, stream=True)
        response.raise_for_status()

        # Determine the content type based on the file extension
        content_type = response.headers.get('Content-Type', 'application/octet-stream')
        file_extension = file_path.split('.')[-1].lower()

        if file_extension in ['pdf', 'jpg', 'txt']:
            # Stream PDF, JPG, and TXT files as usual
            return StreamingResponse(response.iter_content(chunk_size=1024), media_type=content_type)

        elif file_extension == 'docx':
            # Process DOCX file
            doc = Document(io.BytesIO(response.content))
            html_content = "<h3>Preview of DOCX File</h3><div>"
            for para in doc.paragraphs:
                html_content += f"<p>{para.text}</p>"
            html_content += "</div>"
            return HTMLResponse(content=html_content)

        elif file_extension == 'xlsx':
            # Process XLSX file
            workbook = openpyxl.load_workbook(io.BytesIO(response.content), data_only=True)
            sheet = workbook.active
            html_content = "<h3>Preview of XLSX File</h3><table border='1'>"
            for row in sheet.iter_rows(values_only=True):
                html_content += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
            html_content += "</table>"
            return HTMLResponse(content=html_content)

        else:
            # Return a friendly HTML message for unsupported file formats
            return HTMLResponse(content="<h3>Preview not available for this file type</h3>", status_code=200)

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving file: {str(e)}")
