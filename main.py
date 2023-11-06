from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

from apollo import generate_fortune, get_lucky_numbers, generate_image

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

history = {}


@app.get("/")
def read_root():
    return PlainTextResponse("fortune api\n\n~ nathaniel fernandes")


@app.get("/fortune")
async def fortune(req: Request):
    identifier = req.headers.get("X-Forwarded-For", req.client.host)
    currentday = datetime.now().day

    return await gen_fortune(identifier, currentday)


@app.get("/fortune/image")
async def image(req: Request):
    identifier = req.headers.get("X-Forwarded-For", req.client.host)
    currentday = datetime.now().day

    data = await gen_fortune(identifier, currentday)

    if data.get("image_ready", False):
        return data.get("image")

    data["image_ready"] = True

    prompt = data["fortune"]
    img = await generate_image(prompt)

    if img is not None:
        data["image"] = img

    return img


async def gen_fortune(identifier: str, currentday: int):
    h = history.get(identifier, None)
    if h is not None and h["last"] == currentday:
        return h["data"]

    print(f"Generating fortune for {identifier}...")
    fortune, catalyst = await generate_fortune()
    numbers = get_lucky_numbers()
    print(f"Fortune for {identifier} 🔮: {fortune}")

    data = {
        "fortune": fortune,
        "numbers": numbers,
        "theme": catalyst,
        "image": None,
        "image_ready": False,
    }

    history[identifier] = {"last": currentday, "data": data}

    return data
