from databaseStore.video.live_video import LiveVideoRepository

from database import get_db


def get_live_video_repository_manager() -> LiveVideoRepository :
    db = next(get_db())
    return LiveVideoRepository(db)