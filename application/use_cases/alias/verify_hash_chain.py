from application.dtos import HashChainVerificationResponse
from application.dtos.alias_queries import VerifyHashChainQuery
from domain.repositories import IAliasEventRepository
from domain.services import HashChainService
from utils import MESSAGES


class VerifyHashChainUseCase:
    def __init__(
        self,
        alias_event_repository: IAliasEventRepository,
        hash_chain_service: HashChainService,
    ):
        self.alias_event_repository = alias_event_repository
        self.hash_chain_service = hash_chain_service

    def execute(self, query: VerifyHashChainQuery) -> HashChainVerificationResponse:
        alias_normalized = query.alias.strip().lower()

        events = self.alias_event_repository.get_events_for_alias(
            alias_normalized, query.tenant_id
        )

        if not events:
            return HashChainVerificationResponse(
                alias=alias_normalized,
                is_valid=True,
                total_events=0,
                valid_events=0,
                corrupted_events=[],
                chain_break_at=None,
                expected_hash="",
                actual_hash="",
                details=MESSAGES.ERROR.VALIDATION.NO_EVENTS_FOUND_FOR_VERIFICATION.CODE,
            )

        (
            is_valid,
            corrupted_indices,
            chain_break_at,
            expected_hash,
            actual_hash,
        ) = self.hash_chain_service.verify_chain_integrity(events)

        if is_valid:
            details = f"Hash chain integrity verified - all {len(events)} events are consistent"
        else:
            details = f"Chain broken at {len(corrupted_indices)} point(s) - events at indices {corrupted_indices} are corrupted"

        return HashChainVerificationResponse(
            alias=alias_normalized,
            is_valid=is_valid,
            total_events=len(events),
            valid_events=len(events) - len(corrupted_indices),
            corrupted_events=corrupted_indices,
            chain_break_at=chain_break_at,
            expected_hash=expected_hash,
            actual_hash=actual_hash,
            details=details,
        )
