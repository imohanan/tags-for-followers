import sys, json, pprint

def filter_tags(json_data, filter_list):
    filtered_tags = set()
    fixed_list = ["like", "follo", "spam", "shoutout", "comment", "recent"]
    for data in json_data:
        tags = data["tags"]
        for tag in tags:
            if not any(s in tag for s in fixed_list):
                if tag not in filter_list:
                    filtered_tags.add(tag)
    return filtered_tags

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=2)
    input_file = open(sys.argv[1], "r")
    data = input_file.readline()
    filter_list_file = open(sys.argv[2], "r")
    filter_list = []
    for line in filter_list_file:
        filter_list.append(line.strip())
    json_data = json.loads(data)
    #pp.pprint(json_data["data"][0])
    filtered_tags = filter_tags(json_data["data"], filter_list)
    print filtered_tags
