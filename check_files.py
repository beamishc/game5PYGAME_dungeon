
def check_files(player_names):
    '''Asks players to input the number that matches the player name safe file'''
    if len(player_names) == 1:
        return player_names[0]
    else:
        for i, player_name in enumerate(player_names):
            print(f"{i + 1}. {player_name}")
        index = int(input("Which player?\n> ")) - 1

        return player_names[index]
