from fastapi import FastAPI, HTTPException
import zhipuai
from typing import Any

app = FastAPI()

# Set your API key
zhipuai.api_key = "2b1fe5cdbbf2f1ad6b737e1fbfbb87ba.E6a1ZVekEeNnXodT"


@app.post("/ask")
async def ask_model(question: str) -> Any:
    # Invoke the model using the zhipuai library
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_lite",
        prompt=[{"role": "user", "content": question}],
        top_p=0.7,
        temperature=0.9,
    )

    # Collect the responses from the event stream
    result = []
    try:
        for event in response.events():
            if event.event == "add":
                result.append(event.data)
            elif event.event == "error" or event.event == "interrupted":
                raise HTTPException(status_code=400, detail=event.data)
            elif event.event == "finish":
                result.append(event.data)
                return {"result": result, "meta": event.meta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))