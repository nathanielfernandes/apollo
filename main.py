from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from apollo import generate_fortune, get_lucky_numbers

app = FastAPI()
history = {}


@app.get("/")
def read_root():
    return PlainTextResponse("fortune api\n\n~ nathaniel fernandes")


@app.get("/fortune")
async def fortune(req: Request):
    identifier = req.headers.get("X-Forwarded-For", req.client.host)
    currentday = datetime.now().day

    if history.get(identifier, -1) == currentday:
        return {
            "fortune": "You already got your fortune today, come back tomorrow!",
            "numbers": [],
        }

    history[identifier] = currentday

    print(f"Generating fortune for {identifier}...")
    fortune, catalyst = await generate_fortune()
    numbers = get_lucky_numbers()
    print(f"Fortune for {identifier} 🔮: {fortune}")

    return {
        "fortune": fortune,
        "numbers": numbers,
        "theme": catalyst,
    }
