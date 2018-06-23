import os
import sys
import os.path
import importlib.machinery
import unittest


def find_tests_directories(main_path):
    test_dirs = list()
    for root, dirs, files in os.walk(main_path):
        splited = os.path.split(root)
        if splited[-1] in ['test', 'tests']:
            test_dirs.append(os.path.abspath(root))
    return test_dirs


def run_tests():
    main_path = os.path.normpath(os.path.join(sys.path[0]))
    sys.path.append(main_path)
    for test_dir in find_tests_directories(main_path):
        for root, dirs, files in os.walk(test_dir):
            for test_file in files:
                if (test_file.startswith('test_') or test_file.startswith('tests_')) and test_file.endswith('.py'):
                    try:
                        abs_path = os.path.normpath(os.path.join(test_dir, test_file))
                        loader = importlib.machinery.SourceFileLoader(test_file, abs_path)
                        module = loader.load_module()
                        return_code = unittest.main(module, exit=False, verbosity=2)
                        if len(return_code.result.failures) or len(return_code.result.errors):
                            raise Exception("Unit-tests failed.")
                    except BaseException as err:
                        print(test_file)
                        print(err)
                        sys.exit(-1)


if __name__ == '__main__':
    run_tests()
