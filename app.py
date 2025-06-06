from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import subprocess
import os

app = FastAPI()

@app.get("/export/{table_name}")
async def export_table(table_name: str):
    if not table_name.isalnum():
        raise HTTPException(status_code=400, detail="Invalid table name")

    output_path = f"/tmp/{table_name}.csv"

    try:
        result = subprocess.run(
            ["python3", "Export_csv.py", table_name, output_path],
            check=True,
            capture_output=True,
            text=True
        )
        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="File not created")

        return FileResponse(path=output_path, filename=f"{table_name}.csv", media_type="text/csv")

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr)

