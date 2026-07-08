class Mix:
    __listMix = []
    def __init__(self):
        self.__listMix = []

    @property
    def listMix(self):
        return self.__listMix

    def addNote(self, note):
        self.__listMix.append(note)


    def removeNote(self, note):
        self.__listMix.remove(note)