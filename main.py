import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import argparse
import sys

from config import system_prompt
from functions.call_functions import available_functions, call_function

def main():
        #why??
    load_dotenv()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("helpfull message, api key is None")

    client = OpenAI(
        base_url ="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    #define command line arguments
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #create context, for what? It isn't feed to anything
    historic = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        #role? how does it respond without this context? how many roles can you make?
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=historic,
            tools=available_functions,
            temperature=0,
        )

        message = response.choices[0].message
        historic.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = (call_function(tool_call))
                historic.append(result_message)
                if not result_message["content"]:
                    raise Exception("Result is empty")
                if args.verbose == True:
                    print(f"-> {result_message["content"]}")
        #Only work when loop is done
        if response.usage == None:
            raise RuntimeError("helpfull message, something happened, response fucked")
        #print(f"User prompt: {args.user_prompt}")
        #print(f"Prompt tokens: {response.usage.prompt_tokens}")
        #print(f"Response tokens: {response.usage.completion_tokens}")
        if message.content:
            print(f"Final Response: \n{response.choices[0].message.content}")
            break
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
