from fastapi import FastAPI

app = FastAPI()


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
