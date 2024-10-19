
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session 
from models.aiOperations import AIOperations, Rounds
from database import get_db


class  Seed:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db
    def seed_ai_operations(self):
        # Check if the table is empty
        if self.db.query(AIOperations).count() == 0:
            # Create initial data
            initial_data = AIOperations(
                stage_round=Rounds.STAGE1,
                start_audio_processing=False,
            )
            self.db.add(initial_data)
            self.db.commit()
            self.db.refresh(initial_data)
            print("Seeding complete: AIOperations table populated.")
        else:
            print("AIOperations table already populated.")