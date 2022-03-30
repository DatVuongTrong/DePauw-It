from graph_search import bfs, dfs
from dp_street import dp_street
from dp_building import dp_building
from building_choices import building_choices

  # Print out the buildings the users want to go from or go to
building_string = ""
for key, value in building_choices.items():
  building_string += f"{key} - {value}\n"

  # Show the streets which are under maintainece so that the algorithms can choose other routes to go
streets_under_construction = ['Indiana St']

  # Main method for running the program
def depauwit():
  greet()
  new_route(None, None)
  goodbye()

  # Greeting users
def greet():
  print("Hi there and welcome to DePauw!")
  print("We'll help you find the shortest route between the following DePauw buildings:\n" + building_string)

  # Choose the departure and the destination
def set_start_and_end(start_point, end_point):
  if start_point is not None:
    change_point = input("What would you like to change? You can enter 'o' for 'origin', 'd' for 'destination', or 'b' for 'both': ")
    if change_point == "b":
      start_point = get_start()
      end_point = get_end()
    elif change_point == "o":
      start_point = get_start()
    elif change_point == "d":
      end_point = get_end()
    else:
      print("Oops, that isn't 'o', 'd', or 'b'...")
      return set_start_and_end(start_point, end_point)
  else:
    start_point = get_start()
    end_point = get_end()
  return start_point, end_point

  # Get the starting building
def get_start():
  start_point_letter = input("Where are you coming from? Type in the corresponding letter: ")
  if start_point_letter in building_choices:
    start_point= building_choices[start_point_letter]
    return start_point
  else:
    print("Sorry, that's not a building we have data on. Let's try this again...")
    return get_start()
  
  # Get the ending building
def get_end():
  end_point_letter = input("Ok, where are you headed? Type in the corresponding letter: ")
  if end_point_letter in building_choices:
    end_point = building_choices[end_point_letter]
    return end_point
  else:
    print("Sorry, that's not a building we have data on. Let's try this again...")
    return get_end()

  # Find the shortest route to the destination (if there is at least a route)
def new_route(start_point, end_point):
  start_point, end_point = set_start_and_end(start_point,end_point)
  shortest_route = get_route(start_point,end_point)
  if shortest_route:
    shortest_route_string = ' --> '.join(shortest_route)
    print("The shortest route from {0} to {1} is:\n{2}".format(start_point, end_point, shortest_route_string))
  else:
    print("Unfortunately, there is currently no path between {0} and {1} due to maintenance.".format(start_point, end_point))
  again = input("Would you like to see another route? Enter y/n: ")
  if again == "y": 
    show_buildings()
    new_route(start_point, end_point)

  # Option to reshow the lists of buildings
def show_buildings():
  see_landmarks = input("Would you like to see the list of landmarks again? Enter y/n: ")
  if see_landmarks == "y": 
    print(building_string)

def goodbye():
  print("Thanks for using DePauw It!")

  # Algorithm to find the shortest path
def get_route(start_point, end_point):
  start_buildings = dp_building[start_point]
  end_buildings = dp_building[end_point]
  routes = []
  for start_building in start_buildings:
    for end_building in end_buildings:
      street_system = get_active_streets() if streets_under_construction else dp_street
      if streets_under_construction:
        possible_route = dfs(street_system,start_building, end_building)
        if not possible_route: 
          return None
      route = bfs(street_system, start_building, end_building)
      if route == None:
        route = [start_building]  
      routes.append(route)
  shortest_route = min(routes, key=len)
  return shortest_route

  # Update the street systems 
def get_active_streets():
  updated_street = dp_street
  for street_under_construction in streets_under_construction:
    for current_street, neighboring_street in updated_street.items():
        if current_street != street_under_construction:
          updated_street[current_street] -= set(streets_under_construction)
        else:
          current_street = set([])
    return updated_street

depauwit()