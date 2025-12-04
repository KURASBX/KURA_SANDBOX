import hashlib
from datetime import datetime, timezone
from typing import Optional

from core import settings
from domain.entities import AliasEventEntity
from utils import MESSAGES


class HashChainService:
    def __init__(self):
        self.pepper = settings.CUB_PEPPER
        if not self.pepper:
            raise ValueError(MESSAGES.ERROR.AUTH.CUB_PEPPER_NOT_SET.CODE)

    def calculate_cub_hash(
        self,
        tenant_id: str,
        bank: str,
        account_type: str,
        last_4: str,
        alias_normalized: Optional[str] = None,
    ) -> str:
        """Hash pseudonimizado tipo CUB/CUV"""
        material = f"{tenant_id}|{bank}|{account_type}|{last_4}|{alias_normalized or ''}|{self.pepper}"
        return hashlib.sha256(material.encode()).hexdigest()

    def calculate_event_hash(
        self,
        tenant_id: str,
        alias: str,
        event_type: str,
        timestamp: datetime,
        previous_hash: str,
    ) -> str:
        """Hash para eventos de auditoría"""
        if timestamp.tzinfo is not None:
            timestamp = timestamp.astimezone(timezone.utc).replace(tzinfo=None)
        else:
            timestamp = timestamp.replace(tzinfo=None)
        timestamp_str = timestamp.isoformat()
        data = f"{tenant_id}:{alias}:{event_type}:{timestamp_str}:{previous_hash}"

        return hashlib.sha256(data.encode()).hexdigest()

    def verify_chain_integrity(
        self, events: list[AliasEventEntity]
    ) -> tuple[bool, list[int], Optional[int], str, str]:
        """
        Verifica la cadena REAL almacenada
        """
        if not events:
            return True, [], None, "", ""

        corrupted_indices = []
        chain_break_at = None

        if events[0].previous_hash != "0" * 64:
            corrupted_indices.append(0)
            chain_break_at = 0
        else:
            expected_hash_0 = self.calculate_event_hash(
                tenant_id=events[0].tenant_id,
                alias=events[0].alias_normalized,
                event_type=events[0].event_type,
                timestamp=events[0].timestamp,
                previous_hash=events[0].previous_hash,
            )
            if events[0].current_hash != expected_hash_0:
                corrupted_indices.append(0)
                chain_break_at = 0

        for i in range(1, len(events)):
            event = events[i]
            previous_event = events[i - 1]

            if event.previous_hash != previous_event.current_hash:
                corrupted_indices.append(i)
                if chain_break_at is None:
                    chain_break_at = i
                continue

            expected_hash = self.calculate_event_hash(
                tenant_id=event.tenant_id,
                alias=event.alias_normalized,
                event_type=event.event_type,
                timestamp=event.timestamp,
                previous_hash=event.previous_hash,
            )
            if event.current_hash != expected_hash:
                corrupted_indices.append(i)
                if chain_break_at is None:
                    chain_break_at = i

        is_valid = len(corrupted_indices) == 0

        if is_valid:
            expected_final_hash = events[-1].current_hash
            actual_final_hash = events[-1].current_hash
            return (
                is_valid,
                corrupted_indices,
                chain_break_at,
                expected_final_hash,
                actual_final_hash,
            )
        first_corrupt_index = corrupted_indices[0]
        corrupt_event = events[first_corrupt_index]

        if first_corrupt_index == 0:
            expected_hash_0 = self.calculate_event_hash(
                tenant_id=corrupt_event.tenant_id,
                alias=corrupt_event.alias_normalized,
                event_type=corrupt_event.event_type,
                timestamp=corrupt_event.timestamp,
                previous_hash=corrupt_event.previous_hash,
            )
            return (
                is_valid,
                corrupted_indices,
                chain_break_at,
                expected_hash_0,
                corrupt_event.current_hash,
            )
        previous_event = events[first_corrupt_index - 1]
        return (
            is_valid,
            corrupted_indices,
            chain_break_at,
            previous_event.current_hash,
            corrupt_event.previous_hash,
        )
