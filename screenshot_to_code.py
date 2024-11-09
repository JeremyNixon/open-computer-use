import openai
from openai import OpenAI
client = OpenAI(api_key =open('OPENAI_API_KEY.txt').read().strip())

def screenshot_to_code(image_path, instruction):
    prompt = f"""The user's instruction is: \n{instruction}
    Based on this pixel labeled image of a computer screen, write pyautogui code that executes the user's instruction.
    """
    # image_path = "path_to_your_image.jpg"
    
    # Getting the base64 string
    base64_image = encode_image(image_path)
    
    response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt,
            },
            {
              "type": "image_url",
              "image_url": {
                "url":  f"data:image/jpeg;base64,{base64_image}"
              },
            },
          ],
        }
      ],
    )
    return response

