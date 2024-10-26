import os
import requests
import random
import json
from flask import request, jsonify
from pprint import pprint
from ..utils.prompts import USER_CREATE_PROMPT
from ..model import get_register_llm_output, get_customer_llm_output, get_orders_llm_output
from ..db.connection import db
from ..utils.create_payment_link import create_payment_link

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

def payment():
    if request.method == "POST":
        data = request.json
        print(data)
        if (data['type'] == 'payment_intent.succeeded'):
            post_message("Payment successful for ORDER ID 1 by *919324879383*", "917700013317")
            post_message("Payment successful", "919324879383")
            post_message("Share your location for delivery of the merchandise", "919324879383")

            db.whatsapp.update_one({
                "number": "917700013317"
            }, {
                "$push": {
                    "orders": {
                        "product": products[random.randint(0, 3)],
                        "status": "paid"
                    }
                }
            })

            return jsonify("Payment successful")
    return jsonify("Payment failed")

def webhook():
    if request.method == "POST":
        data = request.json
        pprint(data)
        if 'messages' not in data['entry'][0]['changes'][0]['value']: return jsonify("No messages found")
        message_info = data['entry'][0]['changes'][0]['value']['messages'][0]
        
        match message_info['type']:
            case 'text':
                command = message_info['text']['body'].split()[0]
                match command:
                    case '/register':
                        print("HERE BROTHER!")
                        json_data = get_register_llm_output(message_info['text']['body'])
                        client_data = {
                            'enterpriseName': json_data['enterpriseName'],
                            'number': message_info['from'],
                            'email': json_data['email'],
                            'contacts': [],
                            "products": [],
                            "orders": []
                        }
                        db.whatsapp.insert_one(client_data)
                        post_message("Successfully registered!!", message_info['from'])
                        post_message("Now attach contacts to include them into your customer base.", message_info['from'])
                        print("REGISTERED")
                        return jsonify("User created successfully")
                    
                    case '/broadcast':
                        print("BROADCAST", message_info["from"])
                        message = message_info['text']['body'][10:]
                        user = db.whatsapp.find_one({"number": str(message_info['from'])})
                        
                        for contact in user['contacts']:
                            phone_number = contact['phone']
                            post_message(message, phone_number)
                        return jsonify("Broadcasted successfully")
                    
                    case '/order':
                        print("ORDER")
                        message = message_info['text']['body'].split()[1]
                        print(message)
                        if message == "1":
                            link = create_payment_link(message_info['from'])
                            post_message("Please complete the payment on this specific link. " + link, message_info['from'])
                        return jsonify("Order placed successfully")
                    
                    case '/analytics':
                        print("ANALYTICS")
                        user = db.whatsapp.find_one({"number": message_info['from']})
                        if user:
                            orders = user['orders']
                            response = get_orders_llm_output(orders)
                            post_message(response, message_info['from'])
                            return jsonify(response)
                        return jsonify("No orders found")
                    
                    case _:
                        user = db.whatsapp.find_one({"number": message_info['from']})
                        if user:
                            post_message("This is not a valid command, the commands available are:\n \
                                        1. /register _your enterprise name_ and _email_ \n \
                                        2. /broadcast _your message_ \n \
                                        3. /order _order item_", message_info['from'])
                            return jsonify("Invalid command")
                        
                        user = db.whatsapp.find_one({"contacts": {"$elemMatch": {"phone": message_info['from']}}}, {"_id": 0})
                        if not user:
                            post_message("You are not registered, please register first with a merchant first.", message_info['from'])
                            return jsonify("Not registered")
                        
                        userResponse = get_customer_llm_output(message_info['text']['body'], user)
                        post_message(userResponse, message_info['from'])
                        return jsonify("Invalid command")
            case 'location':            
                db.whatsapp.update_one(
                    {'contacts.phone': message_info['from']},
                    {'$set': {'contacts.$[elem].location': message_info['location']}},
                    array_filters=[{'elem.phone': message_info['from']}]
                )
                post_message("Location added successfully", message_info['from'])

                user = db.whatsapp.find_one({"contacts.phone": message_info['from']})
                latitude = message_info['location']['latitude']
                longitude = message_info['location']['longitude']
                post_message("Location of the customer is:", user['number'])
                post_message(f"https://www.google.com/maps?q={latitude},{longitude}", user['number'])

                return jsonify("Location added successfully")

            case 'image':
                # Handle image message
                image_id = data['entry'][0]['changes'][0]['value']['messages'][0]['image']['id']
                print(f"Received image with ID: {image_id}")
                return jsonify("Image received successfully")

            case 'contacts':
                contacts = message_info['contacts']
                contacts_arr = [{
                    "name": contact['name']["formatted_name"],
                    "phone": contact["phones"][0]["wa_id"]
                } for contact in contacts]

                db.whatsapp.update_one(
                    {"number": message_info['from']}, 
                    {"$push": { "contacts": { "$each": contacts_arr } }}
                )
                post_message("Contacts added successfully", message_info['from'])

                return jsonify("Contacts added successfully")
            
            case _:
                return jsonify("Unsupported message type")
    
    return request.args.get('hub.challenge')

def post_message(body: str,phone_number: str):
    print(phone_number)

    headers = {
        'Authorization': f"Bearer {os.environ['WHATSAPP_TOKEN']}",
        'Content-Type': 'application/json'
    }

    data = {
        'messaging_product': 'whatsapp',
        'to': phone_number,
        'type': 'text',
        'text': {'body': body}
    }
    try:
        response = requests.post(os.environ['WHATSAPP_URI'], headers=headers, json=data)
    except Exception as e:
        print(e)

# post_message("Hello", "919324879383")