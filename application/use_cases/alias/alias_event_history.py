from application.dtos import AliasEventHistoryItem, AliasEventHistoryResponse
from application.dtos.alias_event import GetAliasEventHistoryQuery
from domain.repositories.alias_event_repository import IAliasEventRepository


class GetAliasEventHistoryUseCase:
    def __init__(self, alias_event_repository: IAliasEventRepository):
        self.alias_event_repository = alias_event_repository

    def execute(self, query: GetAliasEventHistoryQuery) -> AliasEventHistoryResponse:
        alias_normalized = query.alias.strip().lower()

        events = self.alias_event_repository.get_events_for_alias(
            alias_normalized, query.tenant_id
        )

        event_items = [
            AliasEventHistoryItem(
                event_type=event.event_type,
                timestamp=event.timestamp,
                correlation_id=event.correlation_id,
                previous_hash=event.previous_hash,
                current_hash=event.current_hash,
            )
            for event in events
        ]

        return AliasEventHistoryResponse(
            alias=alias_normalized,
            total_events=len(event_items),
            events=event_items,
        )
