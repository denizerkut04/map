import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fast.api_service import router as fast_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm alan adlarına izin ver
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metodlarına izin ver
    allow_headers=["*"],  # Tüm başlıklara izin ver
)
app.include_router(fast_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        root_cause = ''.join(traceback.format_exception_only(type(exc), exc)).strip()
        return JSONResponse(
            status_code=500,
            content={
                "exception": root_cause
            },
        )
