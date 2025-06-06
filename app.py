from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import psycopg2
import csv
import io

app = FastAPI()


@app.get("/export/{table_name}")
def export_table(table_name: str):
    if not table_name.isidentifier():
        raise HTTPException(status_code=400, detail="Invalid table name")

    try:
        conn = psycopg2.connect(
            dbname="railway",
            user="postgres",
            password="LMJLgMRSLMzOfkaMyXuPPWmmDCBwRVtA",
            host="interchange.proxy.rlwy.net",
            port="40432"
        )
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([desc[0] for desc in cur.description])
        writer.writerows(cur.fetchall())
        cur.close()
        conn.close()

        output.seek(0)

        headers = {
            'Content-Disposition': f'attachment; filename="{table_name}.csv"'
        }
        return StreamingResponse(output, media_type="text/csv", headers=headers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
