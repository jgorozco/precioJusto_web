from frwk.data.DataModel import UserAchievements

ACH_SEEN_GAME='SEEN_GAME'#haz 5 apuestas
ACH_LIKE='LIKE'#haz 15 apuestas
ACH_MONKEY='MONKEY'#haz 25 apuestas

ACH_GOOD_EYE='GOOD_EYE'#acierta 5 seguidas


class ArchievementManager(object):
    
    def setAchievement(self,user,achievement):
        achievement=UserAchievements()
        achievement.user=user
        achievement.achievement=achievement
        achievement.put()