class Node:
    e = None
    d = None
    apar = 0
    char = ''
    
    def __init__(self, e, d, apar, char):
        self.e = e
        self.d = d
        self.apar = apar
        self.char = char
        
    def get_apar(self):
        return self.apar
    def get_char(self):
        return self.char
    def get_e(self):
        return self.e
    def get_d(self):
        return self.d
    
    def set_apar(self, s):
        self.apar = s
    def set_char(self, s):
        self.char = s
    def set_e(self, s):
        self.e = s
    def set_d(self, s):
        self.d = s