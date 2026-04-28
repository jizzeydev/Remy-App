"""Mercado Pago subscription service for Remy platform"""
import os
import uuid
import logging
import mercadopago
from mercadopago.config import RequestOptions
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

# Load .env explicitly
load_dotenv(Path(__file__).parent.parent / '.env')

logger = logging.getLogger(__name__)


# Plan configurations (CLP - Chilean Peso)
PLANS = {
    "monthly": {
        "name": "Plan Mensual Remy",
        "amount": 4990.0,
        "frequency": 1,
        "frequency_type": "months",
        "currency": "CLP"
    },
    "semestral": {
        "name": "Plan Semestral Remy",
        "amount": 19990.0,
        "frequency": 6,
        "frequency_type": "months",
        "currency": "CLP"
    }
}


class MercadoPagoService:
    """Service for Mercado Pago API interactions"""
    
    def __init__(self):
        access_token = os.environ.get('MERCADOPAGO_ACCESS_TOKEN')
        if not access_token:
            logger.warning("MERCADOPAGO_ACCESS_TOKEN not configured")
            self.sdk = None
        else:
            self.sdk = mercadopago.SDK(access_token)
    
    def _get_idempotency_headers(self) -> RequestOptions:
        """Generate idempotency headers for requests"""
        request_options = RequestOptions()
        request_options.custom_headers = {
            'x-idempotency-key': str(uuid.uuid4())
        }
        return request_options
    
    def create_preapproval(
        self,
        plan_id: str,
        payer_email: str,
        card_token: str,
        back_url: str
    ) -> dict:
        """
        Create a subscription (PreApproval) for a customer
        
        Args:
            plan_id: Plan identifier (monthly or semestral)
            payer_email: Customer email
            card_token: Mercado Pago card token
            back_url: URL to redirect after authorization
            
        Returns:
            Response from Mercado Pago API
        """
        if not self.sdk:
            raise Exception("Mercado Pago SDK not configured")
        
        if plan_id not in PLANS:
            raise ValueError(f"Invalid plan_id: {plan_id}")
        
        plan = PLANS[plan_id]
        
        try:
            preapproval_data = {
                "reason": plan["name"],
                "external_reference": f"remy_{plan_id}_{uuid.uuid4().hex[:8]}",
                "payer_email": payer_email,
                "card_token_id": card_token,
                "auto_recurring": {
                    "frequency": plan["frequency"],
                    "frequency_type": plan["frequency_type"],
                    "transaction_amount": plan["amount"],
                    "currency_id": plan["currency"]
                },
                "back_url": back_url,
                "status": "authorized"
            }
            
            result = self.sdk.preapproval().create(
                preapproval_data, 
                self._get_idempotency_headers()
            )
            
            logger.info(f"MP API Response: status={result['status']}, response={result.get('response', {})}")
            
            if result["status"] in [200, 201]:
                logger.info(f"PreApproval created for {payer_email}: {result['response'].get('id')}")
                return result["response"]
            else:
                error_detail = result.get('response', {})
                logger.error(f"Failed to create preapproval: status={result['status']}, response={error_detail}")
                error_message = error_detail.get('message', 'Error desconocido de Mercado Pago')
                if 'cause' in error_detail:
                    causes = error_detail.get('cause', [])
                    if causes:
                        error_message = causes[0].get('description', error_message)
                raise Exception(f"Mercado Pago: {error_message}")
                
        except Exception as e:
            logger.error(f"Error creating preapproval: {str(e)}")
            raise
    
    def get_preapproval(self, preapproval_id: str) -> dict:
        """Get subscription status from Mercado Pago"""
        if not self.sdk:
            raise Exception("Mercado Pago SDK not configured")
        
        try:
            result = self.sdk.preapproval().get(preapproval_id)
            
            if result["status"] == 200:
                return result["response"]
            else:
                logger.error(f"Failed to get preapproval: {result}")
                raise Exception(f"Failed to retrieve subscription: {result}")
                
        except Exception as e:
            logger.error(f"Error getting preapproval: {str(e)}")
            raise
    
    def cancel_preapproval(self, preapproval_id: str) -> dict:
        """Cancel a subscription"""
        if not self.sdk:
            raise Exception("Mercado Pago SDK not configured")
        
        try:
            result = self.sdk.preapproval().update(
                preapproval_id,
                {"status": "cancelled"}
            )
            
            if result["status"] == 200:
                logger.info(f"PreApproval cancelled: {preapproval_id}")
                return result["response"]
            else:
                logger.error(f"Failed to cancel preapproval: {result}")
                raise Exception(f"Failed to cancel subscription: {result}")
                
        except Exception as e:
            logger.error(f"Error cancelling preapproval: {str(e)}")
            raise
    
    def get_plan_info(self, plan_id: str) -> Optional[dict]:
        """Get plan information"""
        return PLANS.get(plan_id)
    
    def list_plans(self) -> list:
        """List all available plans"""
        return [
            {
                "id": plan_id,
                "name": plan["name"],
                "amount": plan["amount"],
                "currency": plan["currency"],
                "frequency": plan["frequency"],
                "frequency_type": plan["frequency_type"]
            }
            for plan_id, plan in PLANS.items()
        ]
