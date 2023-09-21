def check_is_dot_files_the_same(path_one, path_two):
    with open(path_one, "r") as expected_file:
        with open(path_two, "r") as actual_file:
            return sorted(expected_file.readlines()) == sorted(actual_file.readlines())
