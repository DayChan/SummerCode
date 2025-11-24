import os
from langchain_openai.chat_models import ChatOpenAI


def init_chat_model():
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        raise ValueError("ARK_API_KEY is not set. Please set it in your environment variables. 环境变量ARK_API_KEY 没有配置，请在环境变量中配置模型KEY，当前仅支持火山引擎。")
        
    return ChatOpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=api_key,
        model="doubao-seed-code-preview-251028",
        temperature=0,
        max_tokens=8 * 1024,
    )


if __name__ == "__main__":
    chat_model = init_chat_model()
    print(os.environ.get("ARK_API_KEY"))
    print(chat_model.invoke("What is the capital of France?"))