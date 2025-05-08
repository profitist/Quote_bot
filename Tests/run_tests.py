import unittest
from TestFiles import handlers_tests, parse_data_test, quote_maker_test, updates_test

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromModule(handlers_tests))
    suite.addTests(loader.loadTestsFromModule(parse_data_test))
    suite.addTests(loader.loadTestsFromModule(quote_maker_test))
    suite.addTests(loader.loadTestsFromModule(updates_test))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)