#!/usr/bin/env python3
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask(question):
  return openai.Completion.create(model="text-davinci-003", prompt=question, temperature=0, max_tokens=1000)

print(ask("how are you?"))
