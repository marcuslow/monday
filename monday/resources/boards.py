from monday.resources.base import BaseResource
from monday.query_joins import duplicate_board_query, get_boards_query, get_boards_by_id_query, get_board_items_query, \
    get_columns_by_board_query
from monday.resources.types import DuplicateTypes


class BoardResource(BaseResource):
    def __init__(self, token):
        super().__init__(token)

    def fetch_boards(self, **kwargs):
        query = get_boards_query(**kwargs)
        return self.client.execute(query)

    def fetch_boards_by_id(self, board_ids):
        query = get_boards_by_id_query(board_ids)
        return self.client.execute(query)

    def fetch_items_by_board_id(self, board_ids):
        query = get_board_items_query(board_ids)
        return self.client.execute(query)

    def fetch_columns_by_board_id(self, board_ids):
        query = get_columns_by_board_query(board_ids)
        return self.client.execute(query)

    def duplicate_board(self, board_id: int, duplicate_type: DuplicateTypes):
        query = duplicate_board_query(board_id, duplicate_type)
        return self.client.execute(query)
