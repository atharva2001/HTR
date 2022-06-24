import subprocess

def get_result(img):
	command = (f'python main.py --img_file {img}').split()
	process=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)

	process_out= process.communicate()[0]
	process_out=str(process_out)
	return process_out


print(get_result("img.png"))