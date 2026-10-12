from meditracker.database import Session

from meditracker.services.dash_board import get_dash_board

session = Session()

data = get_dash_board(session, 1)
print(data)