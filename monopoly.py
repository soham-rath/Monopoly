import random
import os

print("Welcome to legends of monopoly")

# Define game constants
INITIAL_BALANCE = 1500
START_POSITION = 1

bank = {"bal": 1000000}
players = {
  1: {"name": "", "bal": INITIAL_BALANCE, "pos": START_POSITION, "property": []},
  2: {"name": "", "bal": INITIAL_BALANCE, "pos": START_POSITION, "property": []},
  3: {"name": "", "bal": INITIAL_BALANCE, "pos": START_POSITION, "property": []},
  4: {"name": "", "bal": INITIAL_BALANCE, "pos": START_POSITION, "property": []},
}

#board dictionary
board = {
  1:  ["Shrine of Ressurection(GO)", "0", False],
  2:  ["Temple of Time", "60", True],
  3:  ["Boko Chest", "0", False],
  4:  ["Forest of Spirits", "60", True],
  5:  ["Got insulted by aunty.", "200", False],
  6:  ["Divine Beast VAH MEDOH", "200", True],
  7:  ["Lurelin Village", "100", True],
  8:  ["Chance 1", "0", False],
  9:  ["Rito Village", "100", True],
  10: ["Zora's Domain", "120", True],
  11: ["Lockup(Jail)", "0", False],
  12: ["Goron City", "140", True],
  13: ["HATENO TECH LAB", "150", True],
  14: ["Gerudo Town", "140", True],
  15: ["Korok Forest", "160", True],
  16: ["Divine Beast VAH RUTA", "200", True],
  17: ["Eventide Island", "180", True],
  18: ["Metal Chest", "0", False],
  19: ["Yiga Clan Hideout", "180", True],
  20: ["Satori Mountain", "200", True],
  21: ["Stable(Rest)", "0", False],
  22: ["Spring of Wisdom", "220", True],
  23: ["Chance 2", "0", False],
  24: ["Spring of Power", "220", True],
  25: ["Spring of Courage", "240", True],
  26: ["Divine Beast VAH RUDANIA", "200", True],
  27: ["South Lomei Labyrinth", "260", True],
  28: ["North Lomei Labyrinth", "260", True],
  29: ["AKKALA TECH LAB", "150", True],
  30: ["Lomei Labyrinth", "280", True],
  31: ["Go To LOCKUP", "0", False],
  32: ["Kakariko Village", "300", True],
  33: ["Hateno Village", "300", True],
  34: ["Sheikah Chest", "0", False],
  35: ["Tarrey Town", "320", True],
  36: ["Divine Beast VAH NABORIS", "200", True],
  37: ["Chance 3", "0", False],
  38: ["Forgotten Temple", "350", True],
  39: ["stepped on branch(fall damage).", "100", False],
  0:  ["Hyrule Castle", "400", True]
}

chest = [
  ['Bank error in your favor. Collect $200', 200],
  ['Doctor’s fee. Pay $50', -50], 
  ['From sale of stock you get $50', 50], 
  ['Holiday fund matures. Receive $100', 100], 
  ['Pay hospital fees of $100', -100]
]

chance = [
  ['Bank pays you dividend of $50', 50], 
  ['You have won second prize in a beauty contest. Collect $10', 10], 
  ['Speeding fine $15', -15], 
  ['Your building loan matures. Collect $150', 150], 
  ['You lose $100', -100]
]

properties = {
              2:  {"rent": 2, "rent_h": 10, "rent_2h": 30, "rent_3h": 90,  "rent_4h": 160, "rent_5ht":	250},
              4:  {"rent": 4, "rent_h": 20, "rent_2h": 60, "rent_3h": 180, "rent_4h": 320, "rent_5ht": 450},
              7:  {"rent": 6, "rent_h": 30, "rent_2h": 90, "rent_3h": 270, "rent_4h": 400, "rent_5ht": 550},
              9:  {"rent": 6, "rent_h": 30, "rent_2h": 90, "rent_3h": 270, "rent_4h": 400, "rent_5ht": 550},
              10: {"rent": 8, "rent_h": 40, "rent_2h": 100,"rent_3h": 300, "rent_4h": 450, "rent_ht":	600},
              12: {"rent": 10,"rent_h": 50, "rent_2h": 150,"rent_3h": 450, "rent_4h": 625, "rent_ht": 750},
              14: {"rent": 10,"rent_h": 50, "rent_2h": 150,"rent_3h": 450, "rent_4h": 625, "rent_ht": 750},
              15: {"rent": 12,"rent_h": 60, "rent_2h": 180,"rent_3h": 500, "rent_4h": 700, "rent_ht": 900},
              17: {"rent": 14,"rent_h": 70, "rent_2h": 200,"rent_3h": 550, "rent_4h": 750, "rent_ht": 950},
              19: {"rent": 14,"rent_h": 70, "rent_2h": 200,"rent_3h": 550, "rent_4h": 750, "rent_ht": 950},
              20: {"rent": 16,"rent_h": 80, "rent_2h": 220,"rent_3h": 600, "rent_4h": 800, "rent_ht": 1000},
              22: {"rent": 18,"rent_h": 90, "rent_2h": 250,"rent_3h": 700, "rent_4h": 875, "rent_ht": 1050},
              24: {"rent": 18,"rent_h": 90, "rent_2h": 250,"rent_3h": 700, "rent_4h": 875, "rent_ht": 1050},
              25: {"rent": 20,"rent_h": 100,"rent_2h": 300,"rent_3h": 750, "rent_4h": 925, "rent_ht": 1100},
              27: {"rent": 22,"rent_h": 110,"rent_2h": 330,"rent_3h": 800, "rent_4h": 975, "rent_ht":	1150},
              28: {"rent": 22,"rent_h": 110,"rent_2h": 330,"rent_3h": 800, "rent_4h": 975, "rent_ht":	1150},
              30: {"rent": 24,"rent_h": 120,"rent_2h": 360,"rent_3h": 850, "rent_4h": 1025,"rent_ht": 1200},
              32: {"rent": 26,"rent_h": 130,"rent_2h": 390,"rent_3h": 900, "rent_4h": 1100,"rent_ht": 1275},
              33: {"rent": 26,"rent_h": 130,"rent_2h": 390,"rent_3h": 900, "rent_4h": 1100,"rent_ht": 1275},
              35: {"rent": 28,"rent_h": 150,"rent_2h": 450,"rent_3h": 1000,"rent_4h":	1200,"rent_ht":	1400},
              38: {"rent": 35,"rent_h": 175,"rent_2h": 500,"rent_3h": 1100,"rent_4h":	1300,"rent_ht":	1500},
              0:  {"rent": 50,"rent_h": 200,"rent_2h": 600,"rent_3h": 1400,"rent_4h":	1700,"rent_ht":	2000},

              6:  {"rent": 25,"rent_2": 50,"rent_3": 100,"rent_4": 200},
              16: {"rent": 25,"rent_h": 50,"rent_3": 100,"rent_4": 200},
              26: {"rent": 25,"rent_h": 50,"rent_3": 100,"rent_4": 200},
              36: {"rent": 25,"rent_h": 50,"rent_3": 100,"rent_4": 200},

              13: {"rent": 4,"rent_2": 10},
              29: {"rent": 4,"rent_h": 10},
}


for l in range(1, 5):
        print("What is the name of player", l, "? ")
        players[l]["name"] = input("Type here: ")

#clear console
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
            command = 'cls'
    os.system(command)

#dice roll
def rollDice():
    return random.randint(1, 7) + random.randint(1, 7)

#dispaly info
def displayInfo(player):
  print("Name:", player["name"], "| Balance:", player["bal"], "| Place:", player["pos"], "| Properties:", player["property"])

#transfer money
def transfer(player_from, player_to, amt):
  player_from["bal"] -= amt
  player_to["bal"] += amt

def pressEnterToContinue(text):
    while True:
        user_input = input(text)
        if user_input == "":
            break
#checks if at least 3 players are bankrupt
def checkIfPlayersAreBankrupt():
    bankrupt_players = [player_num for player_num, player in players.items() if player["bal"] <= 0]
    if len(bankrupt_players) >= len(players) - 1:
        print("The game is ending")
        exit()

def buy_property(player, property):
    player["property"].append(property[0])
    property[2] = False
    transfer(player, bank, int(property[1]))

#the main game code
def game(pos, player):
  position = board[pos]
  if position[2] == True:
    print('''
1. Buy the place
2. Display player status
3. Do nothing
        ''')
    print("Enter the option number you want to do. ", end="")
    choice = int(input())
    while (choice != 1 and choice != 2 and choice != 3 and choice != 4):
      choice = input("invalid input, enter again: ")
    if choice == 1:
      player["property"].append(position[0])
      print("Congrats, you bought", position[0])
      position[2] = False
      transfer(player, bank, int(position[1]))
    elif choice == 2:
      displayInfo(player)
      game(pos, player)
    elif choice == 3:
      pass
    else:
        displayInfo(player)
        mortgage_property = input("Which property do you want to mortgage?")
        if player["property"] == mortgage_property:
          print("You mortgaged the property")
  elif pos == 5:
    transfer(player, bank, 200)
    print("You paid 200 to do a therapy lol.")
  elif pos == 39:
    transfer(player, bank, 100)
    print("You paid 100 to visit the doctor, such a failure.")
  else:
    for s in range(1, 5):
      if position[0] in players[s]["property"]:
        property_owner = players[s]["name"]
        rent_amount = properties[current_pos]["rent"]
        if player != players[s]:
          print("This property is owned by", property_owner)
          print("You have to pay rent of $", rent_amount, "to", property_owner)
          transfer(player, players[s], rent_amount)
          displayInfo(players[s])

  displayInfo(player)

while True:
  checkIfPlayersAreBankrupt()
  for i in range(1, len(players)):
    player = players[i]
    clearConsole()
    before_pos = player["pos"]
    print(f"{player['name']}, it is your turn.")
    while input("Press enter to roll the dice. ") != "":
      continue
    else:
      dice_val = rollDice()
      current_pos = before_pos + dice_val
      player["pos"] = current_pos
      if before_pos < 40 and current_pos >= 40:
        player["bal"] += 200
        current_pos -= 40
      print("You rolled a", dice_val)
      print("and you landed on >>", board[current_pos][0])
      if player["pos"] == 11:
        print("You landed at Jail so you can not do anything")
        pressEnterToContinue("Type enter to pass the turn. ")
        continue
      if player["pos"] in [8, 23, 37]:
        chancething = random.choice(chance)
        player["bal"] += chancething[1]
        print(chancething[0])
        displayInfo(player)
        pressEnterToContinue("Type enter to pass the turn. ")
        continue
      if player["pos"] in [3, 18, 34]:
        chestthing = random.choice(chest)
        player["bal"] += chestthing[1]
        displayInfo(player)
        print(chestthing[0])
        displayInfo(player)
        pressEnterToContinue("Type enter to pass the turn. ")
        continue
      else:
        game(current_pos, player)
      pressEnterToContinue("Type enter to pass the turn. ")
      continue

