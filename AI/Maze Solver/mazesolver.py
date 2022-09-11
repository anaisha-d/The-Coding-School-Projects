# Standard Queue class
class Queue:
	def __init__(self):
		self.q = []
	def enqueue(self, val):
		self.q.append(val)
	def dequeue(self):
		if self.size() == 0:
			return None
		else:
			return self.q.pop(0)	
	def peek(self):
		if self.size() == 0:
			return None
		return self	
	def size(self):
		return len(self.q)

# Standard Path Class
class Path:
	def __init__(self, existing_path, next_node):
		self.path = list()		
		if existing_path is None:
			self.path.append(next_node)
		else:
			self.path = existing_path.get_node_list()
			self.path.append(next_node)

	def get_last_node_on_path(self):
		return self.path[len(self.path)-1]
	
	def get_node_list(self):
		return self.path.copy()
	
	def print_path(self, game_board):
		move_locations = list()
		for path_elt in self.path:
			move_locations.append(path_elt.node_val)
		
		top = "-" * len(game_board) * 2
		print(top)
		for row in range(len(game_board)):
			print("|", end="")
			for col in range(len(game_board[row])):
				game_board_elt = game_board[row][col]
				
				if game_board[row][col] == " " and (row, col) in move_locations:
					game_board_elt = "@"
				
				print(game_board_elt + " ", end="")
			print("|")
		print(top)

# Standard Node Class
class Node:
  def __init__(self, node_val):
    self.node_val = node_val # Tuple (row, col)
    self.children = list()

  def generate_children(self, game_board):
    row, col = self.node_val
    height = len(game_board)
    width = len(game_board[0])
    if row + 1 < height:
      if game_board[row+1][col] == " ":        
        self.children.append(Node((row+1, col)))
    if row - 1 > 0:
      if game_board[row-1][col] == " ":
        self.children.append(Node((row-1, col)))
    if col + 1 < width:
      if game_board[row][col+1] == " ":
        self.children.append(Node((row, col+1)))
    if col - 1 > 0:
      if game_board[row][col-1] == " ":
        self.children.append(Node((row, col-1)))


# The method below takes in the name of a .txt file as the parameter maze_file
# The second parameter is the (width/height of the maze*2+1).
# For example, a 10x10 maze would have maze_size = 10*2+1 = 21.

# Given some .txt file maze_file, the method converts this maze_file to a
# 2-dimensional array containing "*" and " " characters. * represents a wall
# and " " represents an open location.

# This method then returns this 2-dimensional array
def convert_maze(maze_file, maze_size):
	row, col = 0,0
	col_index = 0
	game_board = [[None for x in range(maze_size)] for y in range(maze_size)]

	with open(maze_file, 'r') as file:
		for line in file:
			col, col_index = 0,0
			for character in line:
				if col_index % 3 == 1:
					col_index += 1	
					continue

				if character == '.':
					game_board[row][col] = "*"
				else:
					game_board[row][col] = " "
				
				col += 1
				col_index += 1
			row += 1

	return game_board

# The method below prints out the maze for a given game_board input
def print_maze(game_board):
	top = "-" * len(game_board) * 2
	print(top)
	for row in game_board:
		print("|", end="")
		for col in row:
			print(col + " ", end="")
		print("|")
	print(top)
  
def bfs(game_board, initial_node, target_node):
  p = Path(None, initial_node)
  q = Queue()
  q.enqueue(p)
  visited = set()
  visited.add(initial_node.node_val)
  while q.size() > 0:
    p = q.dequeue()
    temp = p.get_last_node_on_path()
    if temp.node_val == target_node.node_val:
      return p
    temp.generate_children(game_board)
    for i in temp.children:
      if i.node_val not in visited:
        q.enqueue(Path(p,i))
        visited.add(i.node_val)
  return None

def main():
	#We'll use a maze_size variable since it makes changing the size easier for future mazes
  maze_size = 50
  game_board = convert_maze("mazes/maze_50x50.txt", maze_size*2+1)
  initial = Node((0,0))
  target = Node((maze_size*2, maze_size*2))
  best_path = bfs(game_board, initial, target)
  best_path.print_path(game_board)

if __name__ == '__main__':
	main()
