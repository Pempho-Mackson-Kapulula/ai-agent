import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions,call_function
import sys


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


parser = argparse.ArgumentParser(description="prompts")
parser.add_argument("user_prompt", type=str,help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = genai.Client(api_key=api_key)


def main():
    max_iterations = 20
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for i in range(max_iterations):
        
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents = messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt,temperature=0, tools=[available_functions],),
        )


        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)



        function_responses = []
        if response.usage_metadata:
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            if response.function_calls:
                for function_call in response.function_calls:
                    function_call_result = call_function(function_call, verbose=args.verbose)

                    if not function_call_result.parts:
                        raise Exception("parts list is empty")
                    
                    elif function_call_result.parts[0].function_response == None:
                        raise Exception("function response is None")
                    
                    elif function_call_result.parts[0].function_response.response == None:
                        raise Exception("Invalid response")
                    
                    else:
                        function_responses.append(function_call_result.parts[0])
                        if args.verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
           
            else:
                print(f"Response: {response.text}")
                return


        else:
            raise RuntimeError("usage metadata is returning None")
            
        
        messages.append(types.Content(role="user", parts=function_responses))

        


if __name__ == "__main__":
    main()
