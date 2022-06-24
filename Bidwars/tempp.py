import subprocess
def sub(path):
    command = (f'python "D:\Biddings-master\HTR\src\fullimg_preprocess.py" {path}').split()
    process=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
    output=str(process.communicate())
    print(output)
