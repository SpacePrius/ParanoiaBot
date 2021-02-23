import pytest
from backend.paranoia.models import Guild, Complex, User, Troubleshooter, GM, Skill
# Create your tests here.
@pytest.mark.django_db
class DBTests():
    def guild_test():
        g = Guild()
        g.discord_id = 810587524639621160
        return 

