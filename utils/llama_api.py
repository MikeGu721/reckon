import json
import requests
from requests.exceptions import RetryError, Timeout
from retrying import retry

retry_kwargs = {
    'wait_exponential_multiplier': 1000,
    'wait_exponential_max': 10000,
    'stop_max_attempt_number': 3,
    'retry_on_exception': lambda x: isinstance(x, RetryError) or isinstance(x, Timeout)
}


# @retry(**retry_kwargs)
def generate(prompt, model="llama2"):
    r = requests.post('http://localhost:11434/api/generate',
                      json={
                          'model': model,
                          'prompt': prompt,
                          'context': [],
                          'stream': False,
                          "options": {
                              "num_predict": 1000,
                              "top_p": 0.9,
                              "temperature": 0.8
                          }
                      })
    return json.loads(r.content).get('response', '')


# @retry(**retry_kwargs)
def chat(instruct, inputs, model="llama2"):
    r = requests.post('http://localhost:11434/api/chat',
                      json={
                          'model': model,
                          "options": {
                              "num_predict": 1000,
                              "top_p": 0.9,
                              "temperature": 0.8
                          },
                          "messages": [
                              {
                                  "role": "assistant",
                                  "content": instruct
                              },
                              {
                                  "role": "user",
                                  "content": inputs
                              }
                          ],
                          'stream': False
                      })
    return json.loads(r.content)['message']['content']


if __name__ == '__main__':
    print(chat('', 'hello'))
