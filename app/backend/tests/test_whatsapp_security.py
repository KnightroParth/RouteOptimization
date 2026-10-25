import unittest
from unittest.mock import patch

from app.services.whatsapp import (
    generate_direct_whatsapp_url,
    send_sandbox_whatsapp_message,
)


class WhatsAppSecurityTests(unittest.IsolatedAsyncioTestCase):
    def test_direct_link_rejects_invalid_phone(self):
        with self.assertRaises(ValueError):
            generate_direct_whatsapp_url("not-a-phone", "Hello")

    def test_direct_link_rejects_empty_message(self):
        with self.assertRaises(ValueError):
            generate_direct_whatsapp_url("+919876543210", "")

    @patch("app.services.whatsapp.DEFAULT_TEST_RECIPIENT", "+919876543210")
    async def test_sandbox_rejects_non_configured_recipient(self):
        with self.assertRaises(ValueError):
            await send_sandbox_whatsapp_message(
                "+919999999999",
                "Test message",
            )


if __name__ == "__main__":
    unittest.main()