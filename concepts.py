class Bacteria:
    def __init__(self, species, gram_stain="gs", motility="mt", habitat="ht", temperature_range="tr", pathogenicity="pg"):
        self.species = species
        # self.gram_stain = gram_stain
        # self.motility = motility
        # self.habitat = habitat
        # self.temperature_range = temperature_range
        # self.pathogenicity = pathogenicity

    def grow(self, nutrients):
        print(f"{self.species} is growing with {nutrients}")

# When a class is defined it becomes the object
print("Bacteria Class", Bacteria) # Bacteria class is a class object  #<class '__main__.Bacteria'>
print(Bacteria.grow) #<function Bacteria.grow at 0x00000221242C9080>
bacObj=Bacteria("Spiralli")
print(bacObj.grow("nutrients")) #Spiralli is growing with nutrients
print(bacObj.grow) #<bound method Bacteria.grow of <__main__.Bacteria object at 0x00000221242D5210>> # this method is bound to bacteria class instance
from datetime import datetime
print(datetime.now)
import time
print(time.time())
print(datetime.now().date())