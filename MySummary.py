from tabulate import tabulate
from manager import Manager
from player import Player
import time
from overall import *
from math import log10, floor
import numpy as np

manager_id = input('What is your FPL ID?')
manager = Manager(manager_id, range(1,14))
manager_name = manager.getName()

### Overall points
print(f"{manager_name[0]}, welcome to the summary of your 2020/21 FPL Season!")
print()
time.sleep(3)

overall_points = manager.getOverallPoints()
overall_rank = manager.getOverallRank()
previous_season_points = manager.getPastSeasonData()
previous_season_points.append({'season_name': '2020/21', 'total_points': overall_points, 'rank': overall_rank})
sorted_previous_season_points = sorted(previous_season_points, key=lambda p: p['rank'])


print(f"You managed to get {overall_points} points this year and finished with a final rank of {overall_rank}!")
time.sleep(3)
print()
print("Now let's see how that fits into your performances from throughout the years!")
time.sleep(3)
print(tabulate(sorted_previous_season_points, headers="keys", colalign=['center','center','center'], numalign='center'))

time.sleep(5)
total_managers = getNumManagers()
percent = round((overall_rank / total_managers)*100, -int(floor(log10(abs((overall_rank / total_managers)*100)))))
if percent >= 1:
    percent = int(percent)

print(f"Your rank of {overall_rank} out of a total {total_managers} managers puts you in the top {percent}% of managers this year")

time.sleep(3)
print('FPL is sweeter when you can beat your friends! Here is how you did in your mini leagues this year...')
print()
time.sleep(3)

###Mini Leagues
mini_leagues = manager.MiniLeagueSummary()
mini_leagues_ranks = [league['rank'] for league in mini_leagues]

best_rank = min(mini_leagues_ranks)
num_wins = mini_leagues_ranks.count(1)
points_off_top = [l['standings']['results'][0]['total'] - overall_points
                  if (l['standings']['results'][0]['total'] - overall_points) != 0
                  else  l['standings']['results'][1]['total'] - overall_points
                  for l in mini_leagues]

leagues_won = [mini_leagues[m]['league_name'] for m in list(np.where(np.array(mini_leagues_ranks)==1)[0]) if len(list(np.where(np.array(mini_leagues_ranks)==1)))>0]


if num_wins > 0: #if they've won any of their leagues
    biggest_win = min(points_off_top)
    biggest_win_league_name = mini_leagues[points_off_top.index(biggest_win)]['league_name']
    second_place = mini_leagues[points_off_top.index(biggest_win)]['standings']['results'][1]['player_name']
    print(f"Out of all of your mini leagues, you managed to win {num_wins} of them!")
    time.sleep(3)
    print(f"That's impressive, you won {','.join(leagues_won)}!")
    time.sleep(3)
    print(f"Your biggest win came in {biggest_win_league_name} where you won by {-biggest_win} points!")
    time.sleep(3)
    print(f"Make sure to tell {second_place} that you beat them to the title in that one...")

else:
    closest = min([p for p in points_off_top if p >=0])
    closest_league_name = [mini_leagues[m]['league_name'] for m in list(np.where(np.array(points_off_top)==closest)[0])]
    winner = mini_leagues[points_off_top.index(closest)]['standings']['results'][0]['player_name']
    print("So...you didn't win any of your mini-leagues this year")
    time.sleep(3)
    print(f"You came closest in {closest_league_name[0]} where you were {closest} points off of {winner} in first!")
    time.sleep(3)
    if closest <=10:
        print("So close! You'll have to get payback next year!")
    elif closest > 100:
        print("More than 100 points off...maybe more work needed for next year")

