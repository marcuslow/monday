from typing import List, Optional
from monday.resources.base import BaseResource
from monday.query_joins import (
    get_boards_query,
    get_boards_by_id_query,
    #get_board_items_query, fucking dead
    get_columns_by_board_query,
    create_board_by_workspace_query,
    get_items_page_query, #marcus
    get_groups_by_board_query, #marcus
    get_updates_for_item_query #marcus
)
from monday.resources.types import BoardKind, BoardState, BoardsOrderBy


class BoardResource(BaseResource):
    def __init__(self, token):
        super().__init__(token)

    def fetch_boards(self, limit: int = None, page: int = None, ids: List[int] = None, board_kind: BoardKind = None, state: BoardState = None, order_by: BoardsOrderBy = None):
        query = get_boards_query(limit, page, ids, board_kind, state, order_by)
        return self.client.execute(query)

    def fetch_boards_by_id(self, board_ids):
        query = get_boards_by_id_query(board_ids)
        return self.client.execute(query)

    """
    def fetch_items_by_board_id(self, board_ids, limit: Optional[int]=None, page: Optional[int]=None):
        #query = get_board_items_query(board_ids, limit=limit, page=page)
        query = get_items_page_query(board_ids)
        return self.client.execute(query)
    """
    
    # marcus
    def fetch_items_by_board_id(self, board_id, limit: Optional[int] = 500, cursor: Optional[str] = None):
        query = get_items_page_query(board_id, limit, cursor)
        response = self.client.execute(query)

        # response["data"]["next_items_page"]["cursor"]
        # response["data"]["next_items_page"]["items"]

        if not cursor :
            items = response["data"]["boards"][0]["items_page"]["items"]
            next_cursor = response["data"]["boards"][0]["items_page"]["cursor"]
        else :
            items = response["data"]["next_items_page"]["items"]
            next_cursor = response["data"]["next_items_page"]["cursor"]

        return items, next_cursor
    
    # marcus
    def fetch_item_update(self, item_id, limit = 100) :
        query = get_updates_for_item_query(item_id=item_id, limit=limit)
        return self.client.execute(query)

    def fetch_columns_by_board_id(self, board_ids):
        query = get_columns_by_board_query(board_ids)
        return self.client.execute(query)

    def create_board(self, board_name: str, board_kind: BoardKind, workspace_id: int = None):
        query = create_board_by_workspace_query(board_name, board_kind, workspace_id)
        return self.client.execute(query)
    
    # marcus
    def fetch_groups_by_board_id(self, board_id):
        query = get_groups_by_board_query(board_id)
        response = self.client.execute(query)
        # Assuming the response structure is similar to what you've described before
        groups = response["data"]["boards"][0]["groups"]
        return groups
