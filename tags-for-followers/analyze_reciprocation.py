import sys, json
import matplotlib.pyplot as plt

if __name__ == "__main__":
    day_1_file = open('data/users/original_users/users_11-08-15.json')
    day_n_file_1 = open('data/users/original_users/users1_11-15-15.json')
    day_n_file_2 = open('data/users/original_users/users2_11-15-15.json')

    day_1_map = json.loads(day_1_file.readline())

    day_n_map = json.loads(day_n_file_1.readline())
    day_n_map_2 = json.loads(day_n_file_2.readline())

    day_n_map.update(day_n_map_2)

    follower_diff_map = []
    follows_diff_map = []

    my_map = {}

    for key in day_n_map:
        final_follower_count = day_n_map[key]["counts"]["followed_by"]
        initial_follower_count = day_1_map[key]["counts"]["followed_by"]

        final_follows_count = day_n_map[key]["counts"]["follows"]
        initial_follows_count = day_1_map[key]["counts"]["follows"]
    
        follower_diff_map.append(final_follower_count - initial_follower_count)
        follows_diff_map.append(final_follows_count - initial_follows_count)
        my_map[final_follows_count - initial_follows_count] = key

    plt.scatter(follows_diff_map, follower_diff_map)
    plt.show()

    sorted_data = sorted(follows_diff_map)
    print my_map[sorted_data[0]]
    print sorted_data[0]

    print day_1_map[my_map[sorted_data[0]]]["username"]

    print day_1_map[my_map[sorted_data[0]]]["counts"]["follows"]
    print day_n_map[my_map[sorted_data[0]]]["counts"]["follows"]
    print day_1_map[my_map[sorted_data[0]]]["counts"]["followed_by"]
    print day_n_map[my_map[sorted_data[0]]]["counts"]["followed_by"]
