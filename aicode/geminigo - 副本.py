from litellm import completion
import os


os.environ['GEMINI_API_KEY'] = "youcode"
response = completion(
    model="gemini/gemini-2.5-flash",
    messages=[{"role": "user", "content": "who r u,name?"}]
)
#print(response)
if response and response.choices and len(response.choices) > 0:
    # 提取 content 文本
    content_text = response.choices[0].message.content
    print("--- 提取到的内容 ---")
    print(content_text)
    print("--------------------")
else:
    print("响应中没有找到预期的内容。")