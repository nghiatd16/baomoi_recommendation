from data_definition.models import News, User, Clicks
from datetime import datetime

news_metadata = {
    "title": "Test title", 
    "category": "Giáo dục",
    "body": "Test body",
    "keywords": ["tét 1", "tét 2"],
    "description": "tét description",
    "publish_timestamp": round(datetime.now().timestamp() * 1000)
}

user_metadata = {
    "username": "nghiatd",
    "password": "test_password"
}

test_user = User(**user_metadata)
test_user.save()


test_news = News(**news_metadata)
test_news.save()

click_metadata = {
    "userid": test_user._id,
    "newsid": test_news._id,
    "timestamp": round(datetime.now().timestamp() * 1000)
}
test_click = Clicks(**click_metadata)
test_click.save()