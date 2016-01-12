from collections import defaultdict

import math

import operator

file_path = "/Users/Brooklyn/PycharmProjects/resys/ml-100k/u.data"

user_item_map = defaultdict(set)
item_user_map = defaultdict(set)

cr = defaultdict()
user_item_count = defaultdict()

similarity_matrix = defaultdict()

def load_file(file_path):
  with open(file_path) as f:
    for line_terminated in f:
      line = line_terminated.rstrip('\n')
      info = line.split("\t")
      user_id = info[0]
      item_id = info[1]
      user_item_map.setdefault(user_id, set()).add(item_id)
      item_user_map.setdefault(item_id, set()).add(user_id)

def init_cr_matrix():
  for item, users in item_user_map.items():
    for u in users:
      user_item_count.setdefault(u, 0)
      user_item_count[u] += 1
      for v in users:
        if (u == v):
          continue
        user_item_count[u] += 1
        cr.setdefault(u, defaultdict()).setdefault(v, 0)
        cr[u][v] += 1

def cal_similariry_matrix():
  for user, related_users in cr.items():
    for related_user, count in related_users.items():
      similarity_matrix.setdefault(user, defaultdict()).setdefault(related_user, 0)
      similarity_matrix[user][related_user] = count / math.sqrt(user_item_count[user] * user_item_count[related_user])

def topN(user):
  rank = defaultdict()
  items = user_item_map[user]
  temp = similarity_matrix[user]
  temp_sorted = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
  for v, wuv in temp_sorted[0: 10]:
    for i in user_item_map[v]:
      if i in items:
        continue
      rank.setdefault(i, 0)
      rank[i] += wuv * 1
  return rank


if __name__ == '__main__':
  load_file(file_path)
  init_cr_matrix()
  cal_similariry_matrix()
  print topN("100")