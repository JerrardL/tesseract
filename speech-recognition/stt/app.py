from os import getenv

from concurrent.futures import ThreadPoolExecutor
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import InvalidUsage

from .engine import SpeechToTextEngine


MAX_ENGINE_WORKERS = int(getenv('MAX_ENGINE_WORKERS', 2))

engine = SpeechToTextEngine()
executor = ThreadPoolExecutor(max_workers=MAX_ENGINE_WORKERS)

app = Sanic()

# Main Route:
# Use POST method with binary and file to upload via Postman
@app.route('/', methods=['POST'])
async def stt(request):
    speech = request.body
    if not speech:
        raise InvalidUsage("Missing \"speech\" payload.")
    from time import perf_counter
    inference_start = perf_counter()
    text = await app.loop.run_in_executor(executor, lambda: engine.run(speech))
    inference_end = perf_counter() - inference_start
    return json({'text': text, 'time': inference_end})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
