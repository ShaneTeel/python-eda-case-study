def update_counts(line, counts_dict):
    for char in line:
        counts_dict['characters'] += 1
        if char == '.':
            counts_dict['sentences'] += 1
        elif char == ' ':
            counts_dict['words'] += 1
    counts_dict['words'] += 1


def create_report(file_path):
    counts_dict = {'sentences': 0, 'words': 0, 'characters': 0}
    with open(file_path) as txt_file:
        for line in txt_file:
            update_counts(line, counts_dict)
    return counts_dict


if __name__ == '__main__':
    print(create_report('test_text.txt'))
