import os, requests

def post_message(body: str):
    headers = {
        'Authorization': 'Bearer EAAFDeDI111oBO6PrMK6TIW3SOFFZBZAsY1uReEJB0asGXYNqyNNVZBA6spGQjYPwesFeaZBZC5Q3Wpb9JKl6Xl3dAb11l3wKt5s09NLohYYjNQu3Ecqqjk0CuVHHgy1ZAvaWRZCilarLWCXsenYCWtpYsSjOEw7spB9q1UYKKRNEkILkr3sWaEVQFBMQKsnzL0BU5byMWrcevn5R6Pc0ZBW3pXbDy1sZD',
        'Content-Type': 'application/json'
    }

    data = {
        'messaging_product': 'whatsapp',
        "to": '917700013317',
        "type": "text",
        "text": { "body": body }
    }

    response = requests.post("https://graph.facebook.com/v20.0/488452314343394/messages", headers=headers, json=data)
    print(response.json())

post_message("hey nice")