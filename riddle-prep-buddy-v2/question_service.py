class QuestionService:

    def __init__(self):
        self.riddles = {
            1: {'clues': ["I may be a circle, a sphere, a line or a curve.",
                          "I am a set of points.",
                          "I am the set of all possible positions a point can take.",
                          "I may be a region in a plane or in space, but more often I am a continuous curve",
                          "I am the path followed by a point subject to some constraint. Who am I"],
                'answers': ["locus"]},
            2: {'clues': ["I am a fluid associated with reptiles, birds and mammals.",
                          "I am a shock absorber but you will never find me in a motor car.",
                          "I also have nothing to do with adults, I prefer embryos.",
                          "I protect the embryo from desiccation and from external pressure.",
                          "I provide a watery environment in which the embryo can develop.",
                          "I am the fluid that surrounds the embryo. Who am I"],
                'answers': ["amniotic fluid"]},
            3: {'clues': ["We are six siblings.",
                          "My siblings and I are not the best sociable family in the community.",
                          "I may be regarded the oldest or youngest depending on what criterion is used",
                          "In terms of weight or mass, I am the lightest.",
                          "My siblings and I hardly mix with others because of the perception that we belong to the noble class.",
                          "I am the second most abundant element in the whole universe. Who am I"],
                'answers': ["helium"]},
            4: {'clues': ["Though I am not a wave, I am described using terms like frequency and period.",
                          "I prefer to move about freely.",
                          "But sometimes I do not have my way when friction appears and dampens my spirits.",
                          "If you can hear a sound, then I am at work inside your ears. Who am I"],
                'answers': ["vibration"]},
        }
        self.reset()

    def get_next_riddle(self, riddle_id):
        try:
            riddle = self.riddles[riddle_id]
        except IndexError as e:
            return None
        return riddle
        
    def reset(self):
        self.current_riddle_id = 1
        self.answered_correctly = False

    def __len__(self):
        return len(self.riddles)

