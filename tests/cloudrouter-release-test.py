import os
import subprocess

# Build Docker container. Load package. Test.

class TestClass:
    def test_build_docker_image(self):
        os.system("sudo docker build -t cloudrouter-release-test .")
        x = subprocess.check_output("sudo docker images", shell=True)
        assert 'cloudrouter-release-test' in x
    def test_run(self):
        x = subprocess.check_output("sudo docker run cloudrouter-release-test yum repolist", shell=True)
        assert 'cloudrouter' in x
        assert 'error' not in x
    def test_cleanup(self):
        os.system("sudo docker rmi -f cloudrouter-release-test")
        x = subprocess.check_output("sudo docker images", shell=True)
        assert 'cloudrouter' not in x

