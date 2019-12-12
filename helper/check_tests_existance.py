'''
Checks whether all module have test-cases written
Call with 'python'

Usage: check_tests_existance.py --module_folder=DIR --tests_folder=DIR

Options:
    --module_folder=DIR     Folder of the modules to be run the check on
    --tests_folder=DIR      Folder where tests are written
'''
import docopt
import os
import glob
import bcolors


def get_list_of_functions(file_name):
    '''Returns the list of functions in a file

    Parameters:
    ----------
    file_name : str
        Path to the file where functions are to be searched

    Returns:
    -------
    list_of_functions : list
        List of function names in the file
    '''
    list_of_functions = []
    with open(file_name, 'rt') as file:
        for line in file:
            if line[0:3] == 'def':
                split_line = line.split(' ')
                split_line = split_line[1].split('(')
                list_of_functions.append(split_line[0])
    return list_of_functions


def find_files_in_directory(folder):
    '''Finds all files with .py extenstion in a folder (but not in subfolders)

    Parameters:
    ----------
    folder : str
        Path to the folder where files are to be searched

    Returns:
    -------
    file_names : list
        list of filenames
    full_paths : list
        list of full paths to the file
    '''
    wild_card_path = os.path.join(folder, '*.py')
    file_names = []
    full_paths = glob.glob(wild_card_path)
    for path in full_paths:
        file_names.append(os.path.basename(path))
    return file_names, full_paths


def compare_tests_with_functions(module_folder, tests_folder):
    module_names, module_paths = find_files_in_directory(module_folder)
    tests_paths = find_files_in_directory(tests_folder)[1]
    missing_files = 0
    missing_tests = 0
    number_functions = 0
    for path, name in zip(module_paths, module_names):
        print(
            bcolors.BOLD + '========== ' + name + ' ==========' + bcolors.ENDC)
        missing_file, missing_test, functions = check_module_test_existance(
            name, tests_folder, tests_paths, path)
        number_functions += len(functions)
        if missing_file == 1:
            for function in functions:
                print(
                    bcolors.WARN
                    + 'Missing test-case for :::'
                    + function
                    + ':::'
                    + bcolors.ENDC)
            missing_test += len(functions)
        if missing_test == 0:
            print(
                bcolors.PASS + 'All functions have test-cases! (Y)'
                + bcolors.ENDC
            )
        missing_files += missing_file
        missing_tests += missing_test
    print('>>>>>>>>>>>>> Summary <<<<<<<<<<<<<')
    print('Modules with no tests: ' + str(missing_files))
    print('Total number tests missing: ' + str(missing_tests))
    print('Total number of functions: ' + str(number_functions))
    percentage_covered = missing_tests/number_functions
    if percentage_covered > 0.9:
        print(
            bcolors.PASS + 'Percentage of tests covered '
            + str(percentage_covered) + bcolors.ENDC
        )
    elif percentage_covered < 0.5:
        print(
            bcolors.ERR + 'Percentage of tests covered '
            + str(percentage_covered) + bcolors.ENDC
        )
    else:
        print(
            bcolors.WARN + 'Percentage of tests covered '
            + str(percentage_covered) + bcolors.ENDC
        )
    print('>>>>>>>>>>>>>> END <<<<<<<<<<<<<<<<<<')


def check_module_test_existance(name, tests_folder, tests_paths, path):
    module_test_file = os.path.join(tests_folder, 'test_' + name)
    missing_file = 0
    missing_test = 0
    module_functions_list = get_list_of_functions(path)
    if not module_test_file in tests_paths:
        missing_file = 1
        print(bcolors.ERR + 'Missing test-file for ' + name + bcolors.ENDC)
    else:
        test_file_functions = get_list_of_functions(module_test_file)
        for module_function in module_functions_list:
            test_name = 'test_' + module_function
            if not test_name in test_file_functions:
                output_string = (
                    'Missing test-case for :::' + module_function + ':::')
                print(bcolors.ERR + output_string + bcolors.ENDC)
                missing_test += 1 
    return missing_file, missing_test, module_functions_list


def main(module_folder, tests_folder):
    module_folder = os.path.expandvars(module_folder)
    tests_folder = os.path.expandvars(tests_folder)
    compare_tests_with_functions(module_folder, tests_folder)



if __name__ == '__main__':
    try:
        arguments = docopt.docopt(__doc__)
        module_folder = arguments['--module_folder']
        tests_folder = arguments['--tests_folder']
        main(module_folder, tests_folder)
    except docopt.DocoptExit as e:
        print(e)

