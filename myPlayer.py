#A card is represented by a string of length 2: (D,C,H,S) + (A,2,3,4,5,6,7,8,9,0,J,Q,K)   "jk" and "JK" respectively mean little king 
# (D,C,H,S) + (A,2,3,4,5,6,7,8,9,0,J,Q,K)   "jk" and "JK" respectively mean little king
import time
import pygame
class Player(object):
	"""docstring for Player"""
	def __init__(self, role, isMy):
		self.roles = ('East', 'North', 'West', 'South')
		self.points = ('5', '10', 'K')
		self.colors = ('D', 'C', 'H', 'S', 'K')
		self.nums = ('A', 'K', 'Q', 'J', '0', '9','8','7','6','5','4','3','2')
		self.nums_order = {num: power for power, num in enumerate(self.nums)}

		self.cards = {color: [] for color in self.colors}
		# record all cards had been pushed out
		self.cards_record = {color: [] for color in self.colors}

		self.role = role
		self.isMy = isMy
		self.main_value = ''
		self.main_color = ''

	def judge_snatch(self):
		main_color = None
		Max = -1
		for color in self.colors:
			if self.main_value in self.cards[color]:
				n = len(self.cards[color])
				if Max < n:
					main_color = color
					Max = n

		if not main_color:
			return ''
		else:
			return main_color + self.main_value

	def add_card(self, current_card, cards):
		# add card
		color, num = current_card
		if color.upper() == 'J':
			cards['K'].append(current_card)
		else:
			cards[color].append(num)

	def remove_card(self, current_card, cards):
		# remove card from cards
		color, num = current_card
		if color.upper() == 'J':
			cards['K'].remove(current_card)
		else:
			cards[color].remove(num)
		
	def add_card_and_is_snatch(self, current_card):
		'''
		Indicates that the player touches a curernt_card and chooses whether to take it or not.
		current_card represents a card (a string of 2 lengths).
		Return the string of the corresponding card if the card is stolen, otherwise return''
		'''
		self.add_card(current_card, self.cards)
		return self.judge_snatch()

	def add_left_cards(self, left_cards):
		'''
		It only needs to be used by the dealer, it means that the bottom card is left_cards, 
		left_cards is a string of 2 and the list returns the card that the player is going to bury
		 in the bottom card, and the list returns a string of 2
		'''
		# left sequence: main_point, point, num_small, main_color_small
		for card in left_cards:
			self.add_card(card, self.cards)
		cards, count = [], 0
		# main_point
		for num in self.cards[self.main_color]:
			card = self.main_color + num
			if num in self.points:
				self.remove_card(card, self.cards)
				cards.append(card)
				if count == 5:
					return cards
				else:
					count += 1

		# point
		for color in self.colors[:-1]:
			for num in self.cards[color]:
				card = color + num
				if num in self.points:
					self.remove_card(card, self.cards)
					cards.append(card)
					if count == 5:
						return cards
					else:
						count += 1

		# num_small
		for color in self.colors[:-1]:
			if color == self.main_color:
				continue
			nums = sorted(self.cards[color], key=lambda num: self.nums_order[num])
			for num in nums:
				card = color + num
				self.remove_card(card, self.cards)
				cards.append(card)
				if count == 5:
					return cards
				else:
					count += 1
		# otherwise
		nums = sorted(self.cards[self.main_color], key=lambda num: self.nums_order[num])
		for num in nums:
			card = self.main_color + num
			self.remove_card(card, self.cards)
			cards.append(card)
			if count == 5:
				return cards
			else:
				count += 1

		return cards

	def finish_one_round(self, current_cards, turn):
		'''
		Denotes the end of the round, the player is informed of the round's play,
		current_turn_out_cards Indicates the list of a triplet (order,role,card).
		Each triplet represents information about a card that someone played before you played that round,
		order is an integer indicating the order in which cards are played (1,2,3,4).
		role is a string representing a role ("banker","banker_opposite","banker_left","banker_right").
		card is a card
		'''
		for card in current_cards:
			self.add_card(card, self.cards_record)

	def set_main_value(self, main_value):
		'''
		Players are told what is the main value, main_value is A character (A, 2,3,4,5,6,7,8,9,0, J, Q, K) says the main value
		'''
		self.main_value = main_value

	def set_main_color(self, main_color):
		'''
		The player is told what the main suit is, and main_color is a character (D,C,H,S) for the main suit
		'''
		self.main_color = main_color

	def player_init(self):
		'''
		Indicates that a new game is now started and the relevant variables are initialized
		'''
		self.main_color = ''
		self.main_value = ''

		for color in self.colors:
			del self.cards[color]
			self.cards[color] =  []

			del self.cards_record[color]
			self.cards_record[color] = []

	def set_role(self, role):
		'''
		The player is told what their role is, and the role is one word("banker","banker_opposite","banker_left","banker_right")
		'''
		self.role = role

	def play_out_cards(self, turn, current_turn_out_cards, background):
		'''
		current_turn_out_cards indicates a list of triples (order,role,card). 
		Each triplet indicates information about a card played by a person
		 before you play in this round. order is an integer. role is a string 
		 that represents the roles ("banker","banker_opposite","banker_left",
		 "banker_right"card is a card function that needs to return the card it decided to play

		color_out, num_out = None, None
		flag = False
		for color in self.colors[:-1]:
			for num in self.cards[color]:
				color_out, num_out = color, num
				flag = True
			if flag:
				card = color_out + num_out
				self.remove_card(card, self.cards)
				return card

		for card in self.cards['K']:
			self.remove_card(card, self.cards)
			return card
		'''
		itme = None
		if(self.isMy):
			#It's your turn to play. Listen for button clicks
			while(True):
				for event in pygame.event.get():
					if  event.type == pygame.MOUSEBUTTONDOWN:
						for it in background.players['South'].get_cards():
							if it.rect.collidepoint(pygame.mouse.get_pos()):
								itme = it
				if itme != None:
					print(itme.face)
					return itme.face

		if turn == 0:
			color_out, num_out, Max = None, None, 0
			for color in self.colors[:-1]:
				if color == self.main_color:
					continue
				n = len(self.cards[color])
				if n > Max:
					color_out = color
					Max = n
			if Max == 0:
				color_out = self.main_color
				Max = len(self.cards[color_out])
			if Max == 0:
				color_out = 'K'
				return self.cards[color_out].pop(0)
			else:
				a, b = self.divide_cards(color_out)
				if len(b) == 0:
					num_out = a[0]
				else:
					num_out = b[len(b)//2]

				self.cards[color_out].remove(num_out)
				print("=======")
				print(color_out + num_out)
				print("=======")
				return	color_out + num_out

		elif turn == 1:
			color_first, num_first = current_turn_out_cards[0]
			if color_first.upper() == 'J':
				return self.random_push_card()
			color_out, num_out = None, None
			Max = len(self.cards[color_first])
			if Max == 0:
				color_out = self.main_color
			else:
				color_out = color_first

			a, b = self.divide_cards(color_out)
			for num in a:
				if self.nums_order[num] > self.nums_order[num_first]:
					num_out = num
					break
			if not num_out:
				if len(b) != 0:
					num_out = b[0]
			if not num_out:
				if len(self.cards['K']) == 0:
					return self.random_push_card()
				else:
					return self.cards['K'].pop(0)
			self.cards[color_out].remove(num_out)
			return color_out + num_out

		elif turn == 2:
			if current_turn_out_cards[0][1] == '5' or current_turn_out_cards[0][1] == '0' or current_turn_out_cards[0][1] == 'K' or current_turn_out_cards[1][1] == '5' or current_turn_out_cards[1][1] == '0' or current_turn_out_cards[1][1] == 'K':
				color = current_turn_out_cards[0][0] if current_turn_out_cards[0][0] not in ['j', 'J'] else 'K'
				if self.cards[color] != []:
					max_num, max_color = '', ''
					for num in self.cards[color]: 
						if max_num == '' or self.nums_order[max_num] > self.nums_order[num]:
							max_num = num
							max_color = color
					self.cards[max_color].remove(max_num)
					return max_color + max_num

				if self.cards['K'] != []:
					card = self.cards['K'][0]
					self.cards['K'].remove(card)
					return card

				if self.cards[self.main_color] != []:
					max_num = ''
					for num in self.cards[self.main_color]:
						if max_num == '' or self.nums_order[max_num] > self.nums_order[num]:
							max_num = num
					self.cards[self.main_color].remove(max_num)
					return self.main_color + max_num

				max_num, max_color = '', ''
				for color in ['H', 'S', 'D', 'C']:
					if self.cards[color] != []:
						for num in self.cards[color]:
							if max_num == '' or self.nums_order[max_num] > self.nums_order[num]:
								max_num = num
								max_color = color
				self.cards[max_color].remove(max_num)
				return max_color + max_num
			else:
				min_num, min_color = '', ''
				for color in ['H', 'S', 'D', 'C']:
					if self.cards[color] != []:
						for num in self.cards[color]:
							if min_num == '' or self.nums_order[min_num] < self.nums_order[num]:
								min_num = num
								min_color = color
				if min_num != '':
					self.cards[min_color].remove(min_num)
					return min_color + min_num

				card = self.cards['K'][0]
				self.cards['K'].remove(card)
				return card
		elif turn == 3:
			if current_turn_out_cards[0][1] == '5' or current_turn_out_cards[0][1] == '0' or current_turn_out_cards[0][1] == 'K' or current_turn_out_cards[1][1] == '5' or current_turn_out_cards[1][1] == '0' or current_turn_out_cards[1][1] == 'K' or current_turn_out_cards[2][1] == '5' or current_turn_out_cards[2][1] == '0' or current_turn_out_cards[2][1] == 'K':
				color = current_turn_out_cards[0][0] if current_turn_out_cards[0][0] not in ['j', 'J'] else 'K'
				if self.cards[color] != []:
					max_num = ''
					for num in self.cards[color]: 
						if max_num == '' or self.nums_order[max_num] > self.nums_order[num]:
							max_num = num
					self.cards[color].remove(max_num)
					return color + max_num

				if self.cards['K'] != []:
					card = self.cards['K'][0]
					self.cards['K'].remove(card)
					return card

				if self.cards[self.main_color] != []:
					max_num = ''
					for num in self.cards[self.main_color]:
						if max_num == '' or self.nums_order[max_num] > self.nums_order[num]:
							max_num = num
					self.cards[self.main_color].remove(max_num)
					return self.main_color + max_num

				max_num, max_color = '', ''
				for color in ['H', 'S', 'D', 'C']:
					if self.cards[color] != []:
						for num in self.cards[color]:
							if max_num == '' or self.nums_order[max_num] > self.nums_order[num]:
								max_num = num
								max_color = color

				self.cards[max_color].remove(max_num)
				return max_color + max_num
			else:
				min_num, min_color = '', ''
				for color in ['H', 'S', 'D', 'C']:
					if self.cards[color] != []:
						for num in self.cards[color]:
							if min_num == '' or self.nums_order[min_num] < self.nums_order[num]:
								min_num = num
								min_color = color
				if min_num != '':
					self.cards[min_color].remove(min_num)
					return min_color + min_num
				card = self.cards['K'][0]

				self.cards['K'].remove(card)
				return card

	def random_push_card(self):
		for color in self.colors:
			for num in self.cards[color]:
				self.cards[color].remove(num)
				return color + num 

	def divide_cards(self, color_out):
		cards = self.cards[color_out]
		# a is points cards, b is non-points cards
		a, b = [], []
		for num in cards:
			if num in self.points:
				b.append(num)
			else:
				a.append(num)

		return sorted(a, key=lambda num: self.nums_order[num]), sorted(b, key=lambda num: self.nums_order[num])

	def show_cards(self):
		'''
		Need to return the current player's hand (a list of strings of length 2)
		'''
		cards = []
		for color in self.colors[:-1]:
			for num in self.cards[color].values():
				card = color + num
				cards.append(card)

		for card in self.cards['K']:
			card.append(card)

		return cards
