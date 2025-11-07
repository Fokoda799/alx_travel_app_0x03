import requests
from django.conf import settings
import uuid

class ChapaService:
    """
    This service class encapsulates all Chapa API interactions.
    By separating this logic, we keep our views clean and make the code reusable.
    """
    
    BASE_URL = "https://api.chapa.co/v1"
    
    def __init__(self):
        self.secret_key = settings.CHAPA_SECRET_KEY
        self.headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json'
        }
    
    def initialize_payment(self, amount, email, first_name, last_name, tx_ref, callback_url, return_url):
        """
        Initialize a payment with Chapa.
        
        The tx_ref (transaction reference) is our unique identifier for this payment.
        We generate it using UUID to ensure it's unique across all payments.
        
        Chapa needs to know where to send the user after payment (return_url) and
        where to send the payment result (callback_url).
        """
        
        url = f"{self.BASE_URL}/transaction/initialize"
        
        payload = {
            "amount": str(amount),
            "currency": "ETB",
            "email": email,
            "first_name": "Abdellah",
            "last_name": "Hadid",
            "tx_ref": tx_ref,
            "callback_url": callback_url,
            "return_url": return_url,
            # Customization makes the payment page look professional
            "customization": {
                "title": "Booking Payment",
                "description": "Payment for your booking"
            }
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()  # Raises an exception for 4xx/5xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            # Log the error in production, you'd use proper logging
            print(f"Error initializing payment: {str(e)}")
            print("Response text:", response.text)
            return None
    
    def verify_payment(self, tx_ref):
        """
        Verify the status of a payment with Chapa.
        
        After a user completes (or attempts) payment, we need to check with Chapa
        what actually happened. This prevents fraud where someone might claim they paid.
        """
        
        url = f"{self.BASE_URL}/transaction/verify/{tx_ref}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error verifying payment: {str(e)}")
            print("Response text:", response.text)
            return None