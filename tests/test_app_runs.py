import os
import subprocess
import sys
import unittest


class AppRunTest(unittest.TestCase):
    def test_app_starts_without_error(self):
        env = os.environ.copy()
        env["APP_TEST_MODE"] = "1"
        process = subprocess.run(
            [sys.executable, "app.py"],
            env=env,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertEqual(
            process.returncode,
            0,
            msg=f"app.py exited with {process.returncode}\nSTDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
