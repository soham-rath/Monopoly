import random
import os

class Property:
    def __init__(self, name, price, base_rent, rents_houses=None):
        self.name = name
        self.price = price
        self.owner = None
        self.mortgaged = False
        self.rents_houses = rents_houses or {0: base_rent}
        self.houses = 0  # number of houses (0-5, where 5 = hotel)
    
    def get_rent(self):
        if self.mortgaged or self.owner is None:
            return 0
        return self.rents_houses.get(self.houses, self.rents_houses[0])
    
    def can_build_house(self):
        return self.houses < 5 and not self.mortgaged
    
    def house_cost(self):
        # Simplified: house cost = half the property price
        return self.price // 2
    
    def build_house(self):
        if self.can_build_house():
            self.houses += 1
            return True
        return False
    
    def sell_house(self):
        if self.houses > 0:
            self.houses -= 1
            return True
        return False

class Player:
    def __init__(self, name):
        self.name = name
        self.balance = 1500
        self.position = 0
        self.properties = []
        self.in_jail = False
        self.bankrupt = False
    
    def move(self, steps):
        prev_position = self.position
        self.position = (self.position + steps) % 40
        # Pass GO
        if self.position < prev_position:
            self.balance += 200
            print(f"{self.name} passed GO and collected $200!")
    
    def buy_property(self, prop: Property):
        if prop.owner is None and self.balance >= prop.price:
            self.balance -= prop.price
            prop.owner = self
            self.properties.append(prop)
            print(f"{self.name} bought {prop.name} for ${prop.price}.")
            return True
        else:
            print(f"{self.name} can't buy {prop.name}.")
            return False
    
    def pay_rent(self, prop: Property):
        rent = prop.get_rent()
        if rent > 0 and prop.owner != self:
            print(f"{self.name} needs to pay ${rent} rent to {prop.owner.name} for {prop.name}.")
            if self.balance >= rent:
                self.balance -= rent
                prop.owner.balance += rent
                print(f"{self.name} paid ${rent} rent.")
            else:
                # Simplified bankruptcy: pay what you can, then bankrupt
                print(f"{self.name} cannot pay rent and is bankrupt!")
                prop.owner.balance += self.balance
                self.balance = 0
                self.bankrupt = True
                # Transfer all properties back to bank
                for p in self.properties:
                    p.owner = None
                    p.houses = 0
                self.properties.clear()
    
    def build_house(self, prop: Property):
        cost = prop.house_cost()
        if prop.owner == self and self.balance >= cost and prop.can_build_house():
            prop.build_house()
            self.balance -= cost
            print(f"{self.name} built a house on {prop.name} for ${cost}.")
            return True
        print(f"{self.name} cannot build house on {prop.name}.")
        return False
    
    def sell_property(self, prop: Property):
        if prop in self.properties:
            sale_price = prop.price // 2  # Simplified sale price
            self.balance += sale_price
            prop.owner = None
            prop.houses = 0
            self.properties.remove(prop)
            print(f"{self.name} sold {prop.name} for ${sale_price}.")
            return True
        print(f"{self.name} does not own {prop.name}.")
        return False
    
    def show_status(self):
        print(f"--- {self.name} ---")
        print(f"Balance: ${self.balance}")
        print(f"Position: {self.position}")
        print(f"Properties owned:")
        if not self.properties:
            print(" None")
        else:
            for p in self.properties:
                houses_str = f"{p.houses} houses" if p.houses > 0 else "no houses"
                print(f" - {p.name} ({houses_str})")
        print("-----------------")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def roll_dice():
    return random.randint(1, 6) + random.randint(1, 6)

def get_valid_input(prompt, valid_options):
    while True:
        choice = input(prompt).lower()
        if choice in valid_options:
            return choice
        else:
            print(f"Invalid input. Choose from {valid_options}")

def main():
    # Properties data based on your original list (only the purchasable ones)
    properties_data = {
        0:  ["Hyrule Castle", 400, 50, {0:50,1:200,2:600,3:1400,4:1700,5:2000}],
        2:  ["Temple of Time", 60, 2, {0:2,1:10,2:30,3:90,4:160,5:250}],
        4:  ["Forest of Spirits", 60, 4, {0:4,1:20,2:60,3:180,4:320,5:450}],
        6:  ["Divine Beast VAH MEDOH", 200, 25],  # Utility, simplified rent
        7:  ["Lurelin Village", 100, 6, {0:6,1:30,2:90,3:270,4:400,5:550}],
        9:  ["Rito Village", 100, 6, {0:6,1:30,2:90,3:270,4:400,5:550}],
        10: ["Zora's Domain", 120, 8, {0:8,1:40,2:100,3:300,4:450,5:600}],
        12: ["Goron City", 140, 10, {0:10,1:50,2:150,3:450,4:625,5:750}],
        13: ["HATENO TECH LAB", 150, 4, {0:4,1:10}],
        14: ["Gerudo Town", 140, 10, {0:10,1:50,2:150,3:450,4:625,5:750}],
        15: ["Korok Forest", 160, 12, {0:12,1:60,2:180,3:500,4:700,5:900}],
        16: ["Divine Beast VAH RUTA", 200, 25],
        17: ["Eventide Island", 180, 14, {0:14,1:70,2:200,3:550,4:750,5:950}],
        19: ["Yiga Clan Hideout", 180, 14, {0:14,1:70,2:200,3:550,4:750,5:950}],
        20: ["Satori Mountain", 200, 16, {0:16,1:80,2:220,3:600,4:800,5:1000}],
        22: ["Spring of Wisdom", 220, 18, {0:18,1:90,2:250,3:700,4:875,5:1050}],
        24: ["Spring of Power", 220, 18, {0:18,1:90,2:250,3:700,4:875,5:1050}],
        25: ["Spring of Courage", 240, 20, {0:20,1:100,2:300,3:750,4:925,5:1100}],
        26: ["Divine Beast VAH RUDANIA", 200, 25],
        27: ["South Lomei Labyrinth", 260, 22, {0:22,1:110,2:330,3:800,4:975,5:1150}],
        28: ["North Lomei Labyrinth", 260, 22, {0:22,1:110,2:330,3:800,4:975,5:1150}],
        29: ["AKKALA TECH LAB", 150, 4, {0:4,1:10}],
        30: ["Lomei Labyrinth", 280, 24, {0:24,1:120,2:360,3:850,4:1025,5:1200}],
        32: ["Kakariko Village", 300, 26, {0:26,1:130,2:390,3:900,4:1100,5:1275}],
        33: ["Hateno Village", 300, 26, {0:26,1:130,2:390,3:900,4:1100,5:1275}],
        35: ["Tarrey Town", 320, 28, {0:28,1:150,2:450,3:1000,4:1200,5:1400}],
        36: ["Divine Beast VAH NABORIS", 200, 25],
        38: ["Forgotten Temple", 350, 35, {0:35,1:175,2:500,3:1100,4:1300,5:1500}],
    }

    # Initialize board
    board = [None]*40
    for idx, data in properties_data.items():
        name, price, base_rent = data[0], data[1], data[2]
        rents = data[3] if len(data) > 3 else None
        board[idx] = Property(name, price, base_rent, rents)

    # Players setup
    num_players = 2
    players = []
    for i in range(1, num_players+1):
        name = input(f"Enter name for Player {i}: ")
        players.append(Player(name))

    turn = 0
    while True:
        clear_console()
        current_player = players[turn % num_players]
        if current_player.bankrupt:
            print(f"{current_player.name} is bankrupt and out of the game.")
            turn += 1
            continue

        print(f"--- {current_player.name}'s turn ---")
        print(f"Balance: ${current_player.balance}")
        current_player.show_status()
        input("Press Enter to roll dice...")
        dice = roll_dice()
        print(f"{current_player.name} rolled {dice}.")
        current_player.move(dice)

        pos = current_player.position
        landed_prop = board[pos]

        if landed_prop is None:
            print(f"{current_player.name} landed on a non-property space (position {pos}). Nothing happens.")
        else:
            print(f"{current_player.name} landed on {landed_prop.name}.")

            if landed_prop.owner is None:
                # Ask to buy
                if current_player.balance >= landed_prop.price and landed_prop.price > 0:
                    buy_choice = get_valid_input(f"Do you want to buy {landed_prop.name} for ${landed_prop.price}? (y/n): ", ['y','n'])
                    if buy_choice == 'y':
                        current_player.buy_property(landed_prop)
                else:
                    print("Cannot buy property: either owned or insufficient funds.")
            elif landed_prop.owner == current_player:
                print(f"You own {landed_prop.name}.")
                build_choice = get_valid_input("Do you want to build a house here? (y/n): ", ['y','n'])
                if build_choice == 'y':
                    current_player.build_house(landed_prop)
            else:
                current_player.pay_rent(landed_prop)

        # Allow selling property
        sell_choice = get_valid_input("Do you want to sell any property? (y/n): ", ['y','n'])
        if sell_choice == 'y':
            if not current_player.properties:
                print("You don't own any properties to sell.")
            else:
                print("Your properties:")
                for i, p in enumerate(current_player.properties):
                    print(f"{i+1}. {p.name} (houses: {p.houses}) - Sell price: ${p.price//2}")
                sel = input("Enter property number to sell or 'c' to cancel: ")
                if sel.isdigit():
                    sel = int(sel)
                    if 1 <= sel <= len(current_player.properties):
                        prop_to_sell = current_player.properties[sel-1]
                        current_player.sell_property(prop_to_sell)
                    else:
                        print("Invalid property number.")
                else:
                    print("Canceling sell.")

        input("Press Enter to end your turn...")
        turn += 1

if __name__ == "__main__":
    main()
