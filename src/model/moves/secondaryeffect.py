class SecondaryEffect:
   """Class that represents the secondary effect of a move i.e boosts
   Args:
    target (str): represents the target i.e: enemy, self, double
    stat (str): The name of the stat affected by the secondary effect
    value (int): The stage to decrease/increase the stat
   """ 

   def __init__(self, target:str, stat:str, value:int):
      self.target = target
      self.stat = stat
      self.value = value