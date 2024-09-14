from fastapi import HTTPException


class PaymentNotFound(HTTPException):
    def __init__(self, event_id, payment_id):
        self.status_code = 404
        self.detail = f"Payment {payment_id} in event {event_id} not found"
        super().__init__(status_code=self.status_code, detail=self.detail)
