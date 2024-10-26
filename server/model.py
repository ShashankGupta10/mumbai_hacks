import os, json
from .db.connection import db
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

from bson import ObjectId  # MongoDB's ObjectId class

# Helper function to handle ObjectId serialization
class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        return super().default(obj)

products = [
    {
        'id': 0,
        'name': 'Red Hoodie',
        'price': 1000
    },{
        'id': 1,
        'name': 'Black T-Shirt',
        'price': 599
    },{
        'id': 2,
        'name': 'White Sneakers',
        'price': 1499
    },{
        'id': 3,
        'name': 'Blue Jeans',
        'price': 1200
    }
]

groq_api_key=os.getenv('GROQ_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
llm=ChatGroq(groq_api_key=groq_api_key,
                model_name="llama-3.1-8b-instant")
output_parser=JsonOutputParser()

def get_register_llm_output(input_text):

    prompt=ChatPromptTemplate.from_messages(
        [
            ("system",'''You will be given user prompts that will contain user information. Give output strictly in JSON that contains the keys: "enterpriseName", "email". If you are unable to extract the information, return an empty JSON object with the values of the keys as empty strings Look for names and put it in enterpriseName and email in email. '''),
            ("user", "User Input: {input}"),
        ]
    )

    chain=prompt|llm|output_parser
    out = chain.invoke({"input": input_text})
    print(out)
    return out

def get_customer_llm_output(input_text, client):

    client_info_str = json.dumps(client, indent=2, cls=MongoEncoder)
    products_str = json.dumps(products, indent=2)


    out = llm.invoke(f"system: You will be given user prompts to with that wants to talk to a merchant with the following information: {client_info_str}\n with the following products: {products_str}\n If the query is not related to the products, ask the user to give only business-related queries. give output in JSON that contains response key with the value as the response to the user query. User Input: {input_text}")
    
    print(out)
    return json.loads(out.content)['response']

def get_orders_llm_output(orders): 
    print(orders)
    orders_str = json.dumps(orders, indent=2)

    out = llm.invoke(f"system: You will be given user prompts that will contain orders with similar information. DONT GIVE CODE. Give output in text that contains that basic analytics about sales, buy quantity and analysis of all individual products. User Input: {orders_str}")
    
    print(out.content)
    return out.content