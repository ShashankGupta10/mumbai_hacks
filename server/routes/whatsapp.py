from flask import Blueprint
from ..controllers.whatsapp import webhook, payment

whatsapp = Blueprint("whatsapp", __name__)

whatsapp.add_url_rule("/webhook", view_func=webhook, methods=['GET', 'POST'])
whatsapp.add_url_rule("/payment", view_func=payment, methods=['GET', 'POST'])