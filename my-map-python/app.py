from uvicorn import run

if __name__ == "__main__":
    run("fast:app", host="0.0.0.0", port=5001, reload=True)
