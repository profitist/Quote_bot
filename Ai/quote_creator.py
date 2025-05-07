import httpx
from Ai import text_utils as tu
from dotenv import dotenv_values


LLM_API_KEY = dotenv_values(".env").get("API_TOKEN")


async def get_quote(text: str) -> str | None:
    """Метод отправки запроса в LLM модель Deepseek на поиск цитаты
       промпт на запрос берется из файла prompt.txt"""
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
    with open('Ai/prompt.txt', 'r') as f:
        prompt = f.read() + text + '<|end_of_prompt|>\n'
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "accept": "application/json",
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": "0.7",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data, timeout=60)
            quote_text = await response.json()
            answer = quote_text['choices'][0]['message']['content'].split('</think>')[1]
            return tu.make_quote_message(answer)
        except httpx.ReadTimeout as e:
            return None
