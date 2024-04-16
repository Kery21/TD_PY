import random as r

ENEMY_SPAWN_DATA = [
  {
    #1
    "weak": 0,
    "medium": 0,
    "strong": 0,
    "elite": 0,
    "boss": 0,
    "SP_boss": 1
  },
  {
    #2
    "weak": r.randint(25, 30),
    "medium": 0,
    "strong": 0,
    "elite": 0,
    "boss": 0,
    "SP_boss": 0
  },
  {
    #3
    "weak": 0,
    "medium": r.randint(10, 12),
    "strong": 0,
    "elite": 0,
    "boss": 0,
    "SP_boss": 0
  },
  {
    #4
    "weak": r.randint(25, 35),
    "medium": r.randint(12, 15),
    "strong": 0,
    "elite": 0,
    "boss": 0,
    "SP_boss": 0
  },
  {
    #5
    "weak": r.randint(7, 10),
    "medium": r.randint(3, 5),
    "strong": 0,
    "elite": 0,
    "boss": 1,
    "SP_boss": 0
  },
  {
    #6
    "weak": r.randint(10, 15),
    "medium": r.randint(7, 10),
    "strong": r.randint(3, 5),
    "elite": 0,
    "boss": 0,
    "SP_boss": 0
  },
  {
    #7
    "weak": r.randint(17, 25),
    "medium": r.randint(15, 20),
    "strong": r.randint(5, 7),
    "elite": 0,
    "boss": 0,
    "SP_boss": 0
  },
  {
    #8
    "weak": r.randint(10, 12),
    "medium": r.randint(12, 15),
    "strong": r.randint(5, 7),
    "elite": 0,
    "boss": 0,
    "SP_boss": 0
  },
  {
    #9
    "weak": r.randint(12, 15),
    "medium": r.randint(12, 15),
    "strong": r.randint(7, 10),
    "elite": 0,
    "boss": 0,
    "SP_boss": 0
  },
  {
    #10
    "weak": r.randint(20, 30),
    "medium": r.randint(15, 25),
    "strong": r.randint(5, 7),
    "elite": 0,
    "boss": 0,
    "SP_boss": 1
  },
  {
    #11
    "weak": r.randint(5, 15),
    "medium": r.randint(7, 12),
    "strong": r.randint(5, 7),
    "elite": r.randint(3, 5),
    "boss": 0,
    "SP_boss": 0
  },
  {
    #12
    "weak": 0,
    "medium": 15,
    "strong": 10,
    "elite": 5,
    "boss": 0,
    "SP_boss": 0
  },
  {
    #13
    "weak": 20,
    "medium": 0,
    "strong": 25,
    "elite": 10,
    "boss": 0,
    "SP_boss": 0
  },
  {
    #14
    "weak": 15,
    "medium": 15,
    "strong": 15,
    "elite": 15,
    "boss": 0,
    "SP_boss": 0
  },
  {
    #15
    "weak": 25,
    "medium": 25,
    "strong": 25,
    "elite": 25,
    "boss": 0,
    "SP_boss": 0
  }
]

ENEMY_DATA = {
    "weak": {         
    "health": r.randint(9, 12),               #Health amount
    "speed": 2,                               #Speed of movement
    "cost": r.randint(2, 4),                  #Kill reward
    "unfreeznes": 1,                          #Freezing protection (1 - none, 0.8 - 20% (1 - 0.8 = 0.2 = 20%) freezing protection, 0 - full protection)
    "HP_steal": 1                             #Amount of HP what will be stealed after the end of way  
  },
    "medium": {
    "health": r.randint(15, 17),
    "speed": 3,
    "cost": r.randint(4, 7),
    "unfreeznes": 1,
    "HP_steal": 1
  },
    "strong": {
    "health": r.randint(17, 25),
    "speed": 4,
    "cost": r.randint(7, 10),
    "unfreeznes": r.randint(7, 9) * 0.1,
    "HP_steal": 1
  },
    "elite": {
    "health": r.randint(45, 60),
    "speed": 1.7,
    "cost": r.randint(15, 20),
    "unfreeznes": r.randint(5, 7) * 0.1,
    "HP_steal": 2
  },
    "boss": {
    "health": 250,
    "speed": 2,
    "cost": 100,
    "unfreeznes": 0,
    "HP_steal": 3
  },
    "SP_boss": {
    "health": 100,
    "speed": 3,
    "cost": 200,
    "unfreeznes": r.randint(1, 3) * 0.1,
    "HP_steal": 5
}}

