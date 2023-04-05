import unittest
from unittest.mock import patch
from io import StringIO

from src.app.actions.hello_world import *


class TestHelloWorld(unittest.TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    def test_hello_world(self, mock_stdout):
        hello_world()
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello World!")


if __name__ == "__main__":
    unittest.main()
