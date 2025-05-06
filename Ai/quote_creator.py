import httpx
import main
from Ai import text_utils as tu
LLM_API_KEY = 'io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6ImI0Y2JmMzNlLTQ2NWItNGZiYy04NzM5LTRmODE0ZTUzZGRkNSIsImV4cCI6NDg5OTUzNDUxMX0.B9lb-9so_MQ2JvtmunnthSdtJtQEmw3LF8ynoj-ClJdHrQqCpJPLYCTZUfuqEgrFw6MlBB0G_Gm6PLkH3kwmNw'


async def get_quote(text: str) -> str | None:
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
            quote_text = response.json()
            print(quote_text)
            answer = quote_text['choices'][0]['message']['content'].split('</think>')[1]
            print(answer)
            return tu.make_quote_message(answer)
        except httpx.ReadTimeout as e:
            return None


async def send_wait_message():
    url = main.BASE_URL
