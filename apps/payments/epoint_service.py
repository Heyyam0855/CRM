"""
ePoint Payment Gateway Service
https://epoint.az — Azərbaycan online ödəniş sistemi
"""
import base64
import hashlib
import json
import logging
from decimal import Decimal
from typing import Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class EPointService:
    """ePoint ödəniş gateway xidməti."""

    def __init__(self):
        self.public_key = getattr(settings, 'EPOINT_PUBLIC_KEY', '')
        self.private_key = getattr(settings, 'EPOINT_PRIVATE_KEY', '')
        self.api_url = getattr(settings, 'EPOINT_API_URL', 'https://epoint.az/api/1/')
        self.site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')

    def _generate_signature(self, data_base64: str) -> str:
        """ePoint imza yaradır: SHA1(private_key + data_base64 + private_key)."""
        sign_string = self.private_key + data_base64 + self.private_key
        return hashlib.sha1(sign_string.encode('utf-8')).hexdigest()

    def _encode_data(self, data: dict) -> str:
        """Data-nı Base64 encode edir."""
        json_str = json.dumps(data, ensure_ascii=False)
        return base64.b64encode(json_str.encode('utf-8')).decode('utf-8')

    def initiate_payment(
        self,
        order_id: str,
        amount: Decimal,
        description: str = 'LMS Platform ödənişi',
    ) -> Optional[dict]:
        """
        ePoint ödəniş prosesini başladır.

        Args:
            order_id: Unikal sipariş ID-si (Payment UUID)
            amount: Ödəniş məbləği (AZN)
            description: Ödəniş açıqlaması

        Returns:
            dict: {'redirect_url': '...', 'transaction_id': '...'}
            None: Xəta baş verdikdə
        """
        try:
            data = {
                'public_key': self.public_key,
                'amount': str(amount),
                'currency': 'AZN',
                'language': 'az',
                'order_id': order_id,
                'description': description,
                'success_redirect_url': f'{self.site_url}/payments/epoint/success/',
                'error_redirect_url': f'{self.site_url}/payments/epoint/error/',
                'callback_url': f'{self.site_url}/payments/epoint/callback/',
            }

            data_base64 = self._encode_data(data)
            signature = self._generate_signature(data_base64)

            response = requests.post(
                f'{self.api_url}request',
                json={
                    'data': data_base64,
                    'signature': signature,
                },
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

            if result.get('status') == 'success':
                logger.info(
                    f"ePoint ödəniş başladıldı: order={order_id}, "
                    f"amount={amount} AZN"
                )
                return {
                    'redirect_url': result.get('redirect_url', ''),
                    'transaction_id': result.get('transaction_id', ''),
                }
            else:
                logger.error(
                    f"ePoint xətası: {result.get('message', 'Naməlum xəta')}"
                )
                return None

        except requests.RequestException as e:
            logger.error(f"ePoint API xətası: {e}", exc_info=True)
            return None

    def verify_callback(self, data_base64: str, signature: str) -> Optional[dict]:
        """
        ePoint callback-ini yoxlayır.

        Args:
            data_base64: ePoint-dən gələn data (base64)
            signature: ePoint-dən gələn imza

        Returns:
            dict: Decoded callback data
            None: İmza yanlışdırsa
        """
        expected_signature = self._generate_signature(data_base64)
        if signature != expected_signature:
            logger.warning("ePoint callback imza doğrulanmadı!")
            return None

        try:
            decoded = base64.b64decode(data_base64)
            return json.loads(decoded)
        except (ValueError, json.JSONDecodeError) as e:
            logger.error(f"ePoint callback decode xətası: {e}")
            return None
