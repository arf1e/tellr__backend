from tellr.models.badge import BadgeModel
from tellr.schemas.badge import BadgeSchema
from tellr.db import db
from tellr import app


badge_schema = BadgeSchema()
badge_list_schema = BadgeSchema(many=True)

badges = [
  {
    "title": "Красивый",
    "title_f": "Красивая",
    "emoji": "+1"
  },
  {
    "title": "Милый",
    "title_f": "Милая",
    "emoji": "cat"
  },
  {
    "title": "Хот",
    "title_f": "Хот",
    "emoji": "fire"
  },
  {
    "title": "Скромный",
    "title_f": "Скромная",
    "emoji": "flushed"
  },
  {
    "title": "Тусовщик",
    "title_f": "Тусовщица",
    "emoji": "tada"
  },
  {
    "title": "Творческий",
    "title_f": "Творческая",
    "emoji": "art"
  },
]

def load_badges():
  with app.app_context():
    db.create_all()
    db.session.bulk_save_objects(badge_list_schema.load(badges))
    db.session.commit()
