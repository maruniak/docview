from pathlib import Path
import subprocess
import os

def convert_to_pdf(input_path: Path, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(output_path.parent),
        str(input_path)
    ])
    if result.returncode != 0:
        raise RuntimeError(f"Failed to convert {input_path} to PDF")

def list_documents(directory: Path):
    return [
        {"filename": file.name, "size": file.stat().st_size}
        for file in directory.glob("*")
        if file.is_file()
    ]
