import stripe

# Replace 'your_secret_key_here' with your actual Stripe secret key
stripe.api_key = 'sk_test_51QDxVUFYeRPvSvRA1BcvmbWuUyciMEYAWdMGdsU6WlYmJkPSEGwKsJISyTFrnFgUwF1jCvCruN7BFsGtaBNmeaqG0024byToF3'

def create_payment_link(number: str):
    try:
        # Step 1: Create a Product
        product = stripe.Product.create(
            name="Red Hoodie",
        )

        # Step 2: Set the Price for the Product
        price = stripe.Price.create(
            product=product.id,
            unit_amount=100000,  # Amount in cents, e.g., 5000 cents for $50.00
            currency='inr',
        )

        # Step 3: Generate the Payment Link 
        payment_link = stripe.PaymentLink.create(
            line_items=[
                {"price": price.id, "quantity": 1},
            ],
            metadata={
                "number": number
            }
        )

        print("Payment Link URL:", payment_link.url)
        return payment_link.url

    except Exception as e:
        print("Error creating payment link:", e)