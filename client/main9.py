import game

def main(name, pswd):
	oGame = game.GetGame(name=name, pswd=pswd)
	oGame.update()


if __name__ == '__main__':
	main(name='9', pswd='9')
