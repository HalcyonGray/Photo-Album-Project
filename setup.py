import subprocess
import sys

subprocess.run('pip install tk')
subprocess.run('pip install image-quality')
subprocess.run('pip install pysqlite3')

#Lists all installed Python Packages
#reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
#installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
#print(installed_packages)
print()
print('Finished Installing packages, Close and Run Start')

