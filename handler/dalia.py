import random 

class Dalia:
    activities = ["Axe throwing party", "Art class party"]
    
    def is_artist(self):
        return True
    
    def do_you_have_a_pen_or_pencil(self):
        return True
    
    def next_activity(self):
        return self.activities[random.randint(1,3)]
    
    def am_i_invited_to_activity(self, name):
        return name != 'Roman'
    
    def catch_phrase(self):
        return "No dude"
    
    def num_sibilings(self):
        return 2

    def best_friend(self):
        return "Stef"
    
    def favorite_greeting(self):
        return "Slav squat"
    
    
    
    