from fastapi import FASTAPi
from fastapi.middleware.cors import CORSMiddleware


app = FASTAPI(title="AI Insight Dashboard - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origins=["*"],
    allow_origins=["*"],
)


@app.get("/")
def root():
    return {"message":"AI Insight Dashboard backend running"}