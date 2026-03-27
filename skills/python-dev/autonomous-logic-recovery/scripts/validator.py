class Validator:
    def __init__(self, epsilon=0.0):
        self.epsilon = epsilon

    def compare(self, dict1: dict, dict2: dict) -> bool:
        if dict1.keys() != dict2.keys():
            return False
        
        for key in dict1:
            val1 = dict1[key]
            val2 = dict2[key]
            
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                if abs(val1 - val2) > self.epsilon:
                    return False
            elif val1 != val2:
                return False
        
        return True
