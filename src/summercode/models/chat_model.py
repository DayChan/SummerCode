import os
from langchain_openai.chat_models import ChatOpenAI


def init_chat_model():
    return ChatOpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=os.environ.get("ARK_API_KEY"),
        model="doubao-seed-code-preview-251028",
        temperature=0,
        max_tokens=8 * 1024,
    )


if __name__ == "__main__":
    chat_model = init_chat_model()
    print(os.environ.get("ARK_API_KEY"))
    print(chat_model.invoke("What is the capital of France?"))