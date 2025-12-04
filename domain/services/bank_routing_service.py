import re
from typing import Optional


class BankRoutingService:
    """Servicio para mapear nombres de bancos a códigos de routing estándar"""

    def __init__(self):
        self._bank_mappings = self._load_bank_mappings()

    def _load_bank_mappings(self) -> dict[str, str]:
        """Carga mapeo de nombres de bancos a códigos SWIFT/BIC para Chile"""
        return {
            # Bancos chilenos principales
            "banco santander": "BSCHCLRM",
            "banco de chile": "BCHICLRM",
            "banco estado": "BECHCLRM",
            "scotiabank": "SCBLCLRX",
            "banco bci": "BCICCLRM",
            "banco security": "BESGCLRM",
            "banco falabella": "BFALCLRM",
            "banco ripley": "BRIECLR1",
            "banco internacional": "BINCCLRM",
            "banco consorcio": "BCOCCLRM",
            # esto deberia convertirse pronto en un utils externo
        }

    def get_routing_code(self, bank_name: str) -> str:
        """Convierte nombre de banco a código de routing SWIFT/BIC"""
        bank_normalized = bank_name.strip().lower()

        if bank_normalized in self._bank_mappings:
            return self._bank_mappings[bank_normalized]

        for known_bank, swift_code in self._bank_mappings.items():
            if known_bank in bank_normalized or bank_normalized in known_bank:
                return swift_code

        # Código genérico para bancos no mapeados
        return "CLRBCLRX"  # CL=Chile, RB=Routing Bank, CL=Location, RX=Generic

    def get_bank_name_from_routing(self, routing_code: str) -> Optional[str]:
        """Resuelve código de routing a nombre de banco (solo uso interno)"""
        reverse_map = {v: k for k, v in self._bank_mappings.items()}
        return reverse_map.get(routing_code)

    def validate_routing_code(self, routing_code: str) -> bool:
        """Valida que un código de routing tenga formato SWIFT/BIC válido"""
        pattern = r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$"
        return bool(re.match(pattern, routing_code))
