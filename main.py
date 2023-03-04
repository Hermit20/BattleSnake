import random
import typing

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Zain, Joshua, Sabawoon, Victor",  # TODO: Your Battlesnake Username
        "color": "#063970",  # TODO: Choose color
        "head": "smile",  # TODO: Choose head
        "tail": "bolt",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def avoid_self(my_body, possible_moves):
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. {"up": {0,1}, "down":{0,1}, "left":{0,1}, "right":{0,1}}

    return: The list of remaining possible_moves
    """

    remove = []
    for direction, location in possible_moves.items():
        if location in my_body:
            remove.append(direction)

    for direction in remove:
        del possible_moves[direction]

    return possible_moves

def avoid_others(snakes, possible_moves):
    """
    snakes: List of dictionaries of Snakes
    possible_moves: List of strings. Moves to pick from.
            e.g. {"up": {0,1}, "down":{0,1}, "left":{0,1}, "right":{0,1}}
    this list is defined below^^^
    returns the improved list of remaining possible_moves
    """
    remove = []
    for snake in snakes:
        for direction, location in possible_moves.items():
            if location in snake["body"]:
                remove.append(direction)
    
    for direction in remove:
        del possible_moves[direction]
    
    return possible_moves
  

def avoid_walls(board_width, board_height, possible_moves):
    remove = []

    for direction, location in possible_moves.items():
        x_out_range = (location["x"] < 0 or location["x"] == board_width)
        y_out_range = (location["y"] < 0 or location["y"] == board_height)
        if x_out_range or y_out_range:
            remove.append(direction)

    for direction in remove:
        del possible_moves[direction]

    return possible_moves

def avoid_box(my_head, possible_moves):
    rs = []
    ls = []
    up = []
    down = []
    final = []

    var = {
      rs:{
        
      },
      ls:{
      
      },
      up:{},
      down:{
      
      }
    }

    for direction, location in possible_moves.items():
      if location["x"] > my_head["x"]:
        var[rs].append(direction)
      elif location["x"] < my_head["x"]:
        var[ls].append(direction)
      elif location["y"] > my_head["y"]:
        var[up].append(direction)
      elif location["y"] < my_head["y"]:
        var[down].append(direction)
    
    max=0
    for key in var:
      if len(key) > max:
        max = key
      

    return max

def findfood(foods, possible_moves):
  get = []
  findb = False
  #For loop for getting food
  for direction, location in possible_moves.items():
    if location not in foods:
      get.append(direction)
    else:
      findb = True

  if(findb):
    for direction in get:
        del possible_moves[direction]

  return possible_moves


  find = {"up": 100, "down": 100, "left": 100, "right":100}

  # For loop for getting closer to food
  for direction, location in possible_moves.items():
    for food in foods:
      x = location.get("x") - food.get("x")
      y = location.get("y") - food.get("y")
      min_disr = 100
      min_disl = 100
      min_disu = 100
      min_disd = 100
      if(x < 0):
        if(find.get("right") >  -1 * x):
          find["right"] = -1 * x
          min_disr = location
      else:
        if(find.get("left") > x):
          find["left"] = x
        min_disl = location
      if(y < 0):
        if(find.get("up") > -1 * y):
          find["up"] = -1 * y
          min_disu = location
        if(find.get("down") > y):
          find["down"] = y
          min_disd = location

  if(min_disr != 100):
    possible_moves["right"] = min_disr

  if(min_disl != 100):
    possible_moves["left"] = min_disl

  if(min_disu != 100):
    possible_moves["up"] = min_disu

  if(min_disd != 100):
    possible_moves["down"] = min_disd


  return possible_moves

def move(game_state: typing.Dict) -> typing.Dict:

    my_head = game_state["you"]["body"][0]
    my_body = game_state["you"]["body"]

    board_height = game_state["board"]["height"]
    board_width = game_state["board"]["width"]
    snakes = game_state["board"]["snakes"]
    foods = game_state["board"]["food"]

    possible_moves = {
          "up": {
              "x": my_head["x"], 
              "y": my_head["y"] + 1
          }, 
          "down": {
              "x": my_head["x"], 
              "y":my_head["y"] - 1
          }, 
          "left": {
              "x": my_head["x"] - 1, 
              "y":my_head["y"]
          }, 
          "right": {
              "x": my_head["x"] + 1, 
              "y":my_head["y"]
          }, 
      }

    possible_moves = avoid_self(my_body, possible_moves)
    possible_moves = avoid_others(snakes, possible_moves)
    possible_moves = avoid_walls(board_width, board_height, possible_moves)
    possible_moves = findfood(foods, possible_moves)

    if len(possible_moves) > 0:
      possible_moves = list(possible_moves.keys())
      move = random.choice(possible_moves)
    else:
        move = "down"

    print(f"MOVE {game_state['turn']}: {move}")
    return {"move": move}
  
  
# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
