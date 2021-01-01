from tabulate import tabulate
from manager import Manager
from player import Player
import time
from overall import *
from math import log10, floor
import numpy as np
from collections import Counter

current_gw = 16

manager_id = input('What is your FPL ID?')
manager = Manager(manager_id, (1,current_gw))
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
    print(f"That's impressive, you won {', '.join(leagues_won)}!")
    print()
    time.sleep(3)
    print(f"Your biggest win came in {biggest_win_league_name} where you won by {-biggest_win} points!")
    print()
    time.sleep(3)
    print(f"Make sure to tell {second_place} that you beat them to the title in that one...")
    print()
    time.sleep(3)

else:
    closest = min([p for p in points_off_top if p >=0])
    closest_league_name = [mini_leagues[m]['league_name'] for m in list(np.where(np.array(points_off_top)==closest)[0])]
    winner = mini_leagues[points_off_top.index(closest)]['standings']['results'][0]['player_name']
    print("So...you didn't win any of your mini-leagues this year")
    time.sleep(3)
    print(f"You came closest in {closest_league_name[0]} where you were {closest} points off of {winner} in first!")
    print()
    time.sleep(3)
    if closest <=10:
        print("So close! You'll have to get payback next year!")
        print()
    elif closest > 100:
        print("More than 100 points off...maybe more work needed for next year")
        print()
    time.sleep(3)

### Best GW
gw_points = [gw['points'] for gw in manager.getSummaryGWData()['current']]
best_gw_points_index = gw_points.index(max(gw_points)) + 1
best_gw_points = max(gw_points)

gw_ranks = [gw['rank'] for gw in manager.getSummaryGWData()['current']]
best_gw_rank_index = gw_ranks.index(min(gw_ranks)) + 1
best_gw_rank = min(gw_ranks)

print("Now lets look at the highlights of your season!")
time.sleep(3)
print(f"Your highest number of points in a single GW of the year came in GW{best_gw_points_index} "
      f"where you scored {best_gw_points} points!")
print()
time.sleep(3)
if best_gw_points_index == best_gw_rank_index:
    print(f"GW{best_gw_rank_index} was also saw your highest rank in a GW where you finished {best_gw_rank} overall!")
    print()
else:
    print(f"However, GW{best_gw_rank_index} wasn't your best week when it comes to rank...in GW{best_gw_rank_index} you "
          f"were {best_gw_rank} overall!")
    print()
time.sleep(3)

#Hits
hits = manager.getHits()
total_hits = sum(hits)
counts_hits = Counter(hits)
hits_values = counts_hits.keys()
print("As you know, you are only allowed one transfer each week, now let's look at how many points hits you had to take...")
time.sleep(3)
print(f"The points hits you took this season totalled {-total_hits} points")
time.sleep(3)

if len(counts_hits) > 0:
    print("This was composed of:")
    time.sleep(3)
    for key in hits_values:
        if key!=0:
            print(f"{counts_hits[key]}x {key} point hits")
            print()
            time.sleep(3)
else:
    print("No points hits this season! Impressive!")
    print()

#which hit was the best/worst
#investigate transfers where hits were taken

hits_gw = [h>0 for h in hits]
hits_benefit = []
hits_details = [manager.getTransferData()[i] if x else False for i, x in enumerate(hits_gw)]
in_transfers_players = []
out_transfers_players = []

for i, hit in enumerate(hits_details):
    if hit:
        in_transfers_pts = []
        out_transfers_pts = []
        for ids in hit['in']['id']:
            in_transfers_pts.append(Player(ids).getSingleGWData(i+1)['total_points'])
        for ids in hit['out']['id']:
            out_transfers_pts.append(Player(ids).getSingleGWData(i+1)['total_points'])
        hits_benefit.append(sum(in_transfers_pts) - hits[i] - sum(out_transfers_pts))
        in_transfers_players.append(hit['in']['name'])
        out_transfers_players.append(hit['out']['name'])
    else:
        hits_benefit.append(False)
        in_transfers_players.append(False)
        out_transfers_players.append(False)

worst_hit = min([h for h in hits_benefit if not False])
worst_hit_week = hits_benefit.index(worst_hit) + 1
worst_week_in_players = in_transfers_players[hits_benefit.index(worst_hit)]
worst_week_out_players = out_transfers_players[hits_benefit.index(worst_hit)]

best_hit = max([h for h in hits_benefit if not False])
best_hit_week = hits_benefit.index(best_hit) + 1
best_week_in_players = in_transfers_players[hits_benefit.index(best_hit)]
best_week_out_players = out_transfers_players[hits_benefit.index(best_hit)]


print("Sometimes hits go to plan, sometimes they don't...")
time.sleep(3)
print()
print(f"Your most successful hit was in GW {best_hit_week}")
print(f"In this week you transferred out {', and '.join([' '.join(tups) for tups in best_week_out_players])} ")
print(f"for {', and '.join([' '.join(tups) for tups in best_week_in_players])}. ")
print(f"Including the hit, you were {best_hit} points better off!")
print()
print()
time.sleep(5)

print(f"Your least successful hit was in GW {worst_hit_week}")
print(f"In this week you transferred out {', and '.join([' '.join(tups) for tups in worst_week_out_players])} ")
print(f"for {', and '.join([' '.join(tups) for tups in worst_week_in_players])}. ")
print(f"Including the hit, you were {-worst_hit} points worse off!")
print()

# Best period of the season
gw_averages = np.array(getAverageGWScores((1, current_gw)))
manager_gw_scores = np.array([gw['points'] for gw in manager.getSummaryGWData()['current']])
diffs = np.subtract(manager_gw_scores, gw_averages)

partial_sum = sum(diffs[:5])
max_sum = partial_sum
max_ind = 0
min_sum = partial_sum
min_ind = 0

for i, x in enumerate(diffs):
    if i+5 >= len(diffs):
        break
    partial_sum = partial_sum - x + diffs[i+5]
    if partial_sum > max_sum:
        max_sum = partial_sum
        max_ind = i+1
    if partial_sum < min_sum:
        min_sum = partial_sum
        min_ind = i+1

overall_rank_progression = manager.getRanks()
overall_rank_progression.insert(0, 'the start') #insert 0 at the beginning of the list so that element at i is the rank before that GW started

best_period_min = max_ind
best_period_max = max_ind + 4
best_period_rank_from = overall_rank_progression[max_ind]
best_period_rank_to = overall_rank_progression[max_ind+5]

worst_period_min = min_ind
worst_period_max = min_ind + 4
worst_period_rank_from = overall_rank_progression[min_ind]
worst_period_rank_to = overall_rank_progression[min_ind+5]

print("Each season is filled with many ups and downs...now we'll see your best and worst periods of the season!")
time.sleep(5)
print(f"Your best five week period of the season came between GW {best_period_min+1}-{best_period_max+1}")
time.sleep(5)
if max_sum > 0:
    print(f"In this period you were a total of {max_sum} points better than the average, and your rank went from {best_period_rank_from} to {best_period_rank_to}!")
else:
    print(f"Even though it was your best period, in this period you were a total of {max_sum} points worse than the average, and your rank went from {best_period_rank_from} to {best_period_rank_to}!")
time.sleep(5)

print(f"Your worst five week period of the season game between GW {worst_period_min+1}-{worst_period_max+1}")
time.sleep(5)
if min_sum > 0:
    print(f"Even though it was your worst five week period you were still a total of {min_sum} points more than the average. Your rank went from {worst_period_rank_from} to {worst_period_rank_to}")
else:
    print(f"In this period you were a total of {min_sum} points worse than the average, and your rank went from {worst_period_rank_from} to {worst_period_rank_to}")
time.sleep(5)
