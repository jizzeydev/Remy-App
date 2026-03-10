"""
Email notification service for Remy Platform
Uses Resend for transactional emails
"""
import os
import asyncio
import logging
import resend
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# Initialize Resend
resend.api_key = os.environ.get('RESEND_API_KEY')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'onboarding@resend.dev')
ADMIN_EMAIL = os.environ.get('ADMIN_NOTIFICATION_EMAIL', 'seremonta.cl@gmail.com')


async def send_email(to_email: str, subject: str, html_content: str) -> dict:
    """Send email using Resend (non-blocking)"""
    if not resend.api_key:
        logger.warning("RESEND_API_KEY not configured, skipping email")
        return {"status": "skipped", "reason": "API key not configured"}
    
    params = {
        "from": SENDER_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html_content
    }
    
    try:
        # Run sync SDK in thread to keep FastAPI non-blocking
        email = await asyncio.to_thread(resend.Emails.send, params)
        logger.info(f"Email sent to {to_email}: {subject}")
        return {"status": "success", "email_id": email.get("id")}
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return {"status": "error", "error": str(e)}


# ==================== EMAIL TEMPLATES ====================

def get_base_template(content: str) -> str:
    """Base HTML template for all emails"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; background-color: #f4f4f5; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f5; padding: 40px 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #0f172a 0%, #164e63 100%); padding: 30px; text-align: center;">
                                <h1 style="color: #22d3ee; margin: 0; font-size: 28px;">Remy</h1>
                                <p style="color: #94a3b8; margin: 5px 0 0 0; font-size: 14px;">Tu plataforma de estudio inteligente</p>
                            </td>
                        </tr>
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                {content}
                            </td>
                        </tr>
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f8fafc; padding: 20px 30px; text-align: center; border-top: 1px solid #e2e8f0;">
                                <p style="color: #64748b; margin: 0; font-size: 12px;">
                                    © 2026 Remy by Seremonta. Todos los derechos reservados.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


# ==================== NOTIFICATION FUNCTIONS ====================

async def notify_new_user_registration(user_email: str, user_name: str):
    """Notify admin when a new user registers"""
    timestamp = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    
    content = f"""
        <h2 style="color: #0f172a; margin: 0 0 20px 0;">🎉 Nuevo Usuario Registrado</h2>
        <div style="background-color: #f0fdfa; border-left: 4px solid #14b8a6; padding: 15px; margin-bottom: 20px;">
            <p style="margin: 0; color: #0f172a;"><strong>Email:</strong> {user_email}</p>
            <p style="margin: 10px 0 0 0; color: #0f172a;"><strong>Nombre:</strong> {user_name}</p>
            <p style="margin: 10px 0 0 0; color: #64748b; font-size: 13px;">Registrado: {timestamp}</p>
        </div>
        <p style="color: #64748b; margin: 0;">Este usuario se registró con Google en la plataforma Remy.</p>
    """
    
    await send_email(
        ADMIN_EMAIL,
        f"🎉 Nuevo usuario: {user_name}",
        get_base_template(content)
    )


async def notify_subscription_started(user_email: str, user_name: str, plan: str, amount: float):
    """Notify admin when a user starts a subscription"""
    timestamp = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    amount_formatted = f"${amount:,.0f} CLP"
    
    content = f"""
        <h2 style="color: #0f172a; margin: 0 0 20px 0;">💳 Nueva Suscripción</h2>
        <div style="background-color: #ecfdf5; border-left: 4px solid #10b981; padding: 15px; margin-bottom: 20px;">
            <p style="margin: 0; color: #0f172a;"><strong>Usuario:</strong> {user_name} ({user_email})</p>
            <p style="margin: 10px 0 0 0; color: #0f172a;"><strong>Plan:</strong> {plan}</p>
            <p style="margin: 10px 0 0 0; color: #10b981; font-size: 18px;"><strong>Monto:</strong> {amount_formatted}</p>
            <p style="margin: 10px 0 0 0; color: #64748b; font-size: 13px;">Fecha: {timestamp}</p>
        </div>
        <p style="color: #64748b; margin: 0;">El pago fue procesado exitosamente por Mercado Pago.</p>
    """
    
    await send_email(
        ADMIN_EMAIL,
        f"💳 Nueva suscripción: {user_name} - {plan}",
        get_base_template(content)
    )


async def notify_subscription_cancelled(user_email: str, user_name: str, reason: str = ""):
    """Notify admin when a subscription is cancelled"""
    timestamp = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    reason_text = f"<p style='margin: 10px 0 0 0; color: #0f172a;'><strong>Razón:</strong> {reason}</p>" if reason else ""
    
    content = f"""
        <h2 style="color: #0f172a; margin: 0 0 20px 0;">❌ Suscripción Cancelada</h2>
        <div style="background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 15px; margin-bottom: 20px;">
            <p style="margin: 0; color: #0f172a;"><strong>Usuario:</strong> {user_name} ({user_email})</p>
            {reason_text}
            <p style="margin: 10px 0 0 0; color: #64748b; font-size: 13px;">Fecha: {timestamp}</p>
        </div>
        <p style="color: #64748b; margin: 0;">La suscripción ha sido cancelada.</p>
    """
    
    await send_email(
        ADMIN_EMAIL,
        f"❌ Suscripción cancelada: {user_name}",
        get_base_template(content)
    )


async def send_welcome_email(user_email: str, user_name: str):
    """Send welcome email to new user"""
    content = f"""
        <h2 style="color: #0f172a; margin: 0 0 20px 0;">¡Bienvenido a Remy, {user_name}! 🎓</h2>
        <p style="color: #475569; line-height: 1.6;">
            Gracias por unirte a nuestra plataforma de estudio inteligente. 
            Estás a un paso de mejorar tu rendimiento académico.
        </p>
        <div style="background-color: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #0369a1; margin: 0 0 10px 0;">¿Qué puedes hacer ahora?</h3>
            <ul style="color: #475569; margin: 0; padding-left: 20px;">
                <li style="margin-bottom: 8px;">Explorar nuestros cursos disponibles</li>
                <li style="margin-bottom: 8px;">Practicar con simulacros personalizados</li>
                <li style="margin-bottom: 8px;">Suscribirte para acceso completo</li>
            </ul>
        </div>
        <p style="color: #475569; margin-bottom: 25px;">
            Si tienes preguntas, no dudes en contactarnos.
        </p>
        <a href="https://remy.seremonta.store" 
           style="display: inline-block; background-color: #06b6d4; color: #ffffff; padding: 12px 30px; 
                  text-decoration: none; border-radius: 8px; font-weight: bold;">
            Ir a Remy
        </a>
    """
    
    await send_email(
        user_email,
        "¡Bienvenido a Remy! 🎓",
        get_base_template(content)
    )
