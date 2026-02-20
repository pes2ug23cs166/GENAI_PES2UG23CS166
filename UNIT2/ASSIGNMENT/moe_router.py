from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



MODEL_CONFIG = {

    "technical": {

        "system_prompt":
        """You are a Technical Expert.
Give precise debugging help.
Provide coding solutions."""
    },

    "billing": {

        "system_prompt":
        """You are a Billing Expert.
Be empathetic.
Explain refund policies professionally."""
    },

    "general": {

        "system_prompt":
        """You are a friendly assistant."""
    }

}




def route_prompt(user_input):

    router_prompt=f"""
Classify into:

technical
billing
general

Return ONLY the word.

Query:
{user_input}
"""

    response=client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0,

        messages=[

            {
                "role":"system",
                "content":"You are strict classifier."
            },

            {
                "role":"user",
                "content":router_prompt
            }

        ]

    )

    category=response.choices[0].message.content.strip().lower()

    return category




def call_expert(category,user_input):

    system_prompt=MODEL_CONFIG[category]["system_prompt"]

    response=client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0.7,

        messages=[

            {
                "role":"system",
                "content":system_prompt
            },

            {
                "role":"user",
                "content":user_input
            }

        ]

    )

    return response.choices[0].message.content




def bitcoin_price_tool():

    return "Bitcoin price approx $60,000 (Mock Tool Output)"




def process_request(user_input):

    if "bitcoin" in user_input.lower():

        print("\nRouter Selected: tool")

        return bitcoin_price_tool()

    category=route_prompt(user_input)

    print("\nRouter Selected:",category)

    if category not in MODEL_CONFIG:

        category="general"

    return call_expert(category,user_input)




if __name__=="__main__":

    while True:

        query=input("\nAsk Support (exit to stop): ")

        if query.lower()=="exit":

            break

        answer=process_request(query)

        print("\nResponse:\n",answer)