from http.client import HTTPException

from sqlalchemy import desc, literal, select, func, and_
from sqlalchemy.sql import Select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi.responses import FileResponse
from src.auth.auth import get_current_user
from src.auth.models import User
from src.db import get_async_db_session
import os
from yookassa import Configuration
from yookassa import Payment
import uuid
from src.setting import setting as settings

Configuration.account_id = settings.account_id_ukassa
Configuration.secret_key = settings.secret_key_ukassa
# Configuration.configure_auth_token('<Bearer Token>')


class PaymentBooking:

    async def get_contract(self, user: User = Depends(get_current_user)):
        pdf_file_path = f"/documents/contract/contract.pdf"

        # Проверяем, существует ли файл
        if not os.path.exists(pdf_file_path):
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(pdf_file_path, media_type='application/pdf', filename=f"{1_7939}.pdf")

    async def payment(self, amount, user: User = Depends(get_current_user)):
        idempotence_key = str(uuid.uuid4())
        payment = Payment.create({
            "amount": {
                "value": amount,
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://google.com"
            },
            "description": "Order No. 72"
        }, idempotence_key)

        # get confirmation url
        confirmation_url = payment.confirmation.confirmation_url
        payment_id = payment.id
        return confirmation_url


payment_services = PaymentBooking()
