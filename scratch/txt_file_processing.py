def update_counts(line, counts_dict):
    counts_dict["Sentences"] += line.count(".")
    counts_dict["Words"] += len(line.split())
    counts_dict["Characters"] += len(line)

def create_report(file_path):
    counts_dict = {'Sentences': 0, "Words": 0, "Characters": 0}
    with open(file_path) as txt_file:
        for line in txt_file:
            update_counts(line, counts_dict)
    return counts_dict

if __name__ == '__main__':
    print(create_report('test_text.txt'))