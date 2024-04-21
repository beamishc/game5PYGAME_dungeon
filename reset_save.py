import json
import sys

with open('save_file.json') as f:
    save_dct = json.load(f)

save_file = save_dct[sys.argv[1]]

save_file["CURRENT_LEVEL"] = 0
save_file["HIGHEST_LEVEL"] = 0
save_file["TIMES_DIED"] = 0

with open('save_file.json', 'w') as f:
    json.dump(save_dct, f)
