import requests, json, random, os, time
from termcolor import colored
os.system("color")

apiUrl = "https://api.scratch.mit.edu/"
checkProjectUrl = apiUrl + "projects/"
addProjectUrl = apiUrl + "studios/Project ID/project/"

token = open("secret.txt", "r").read()
blockedIds = open("cached-ids.txt", "r").read().splitlines()

writeTo = open("cached-ids.txt", "a")

def write_to_blacklisted(txt):
	blockedIds.append(txt)
	writeTo.write(txt)

def check_project():
	strId = str(random.randint(104, 118_000_000))
	project = checkProjectUrl + strId

	if strId in blockedIds:
		print(colored("|[Status]|: project was considered inactive or was added in the studio!", "yellow"))
		return False

	print(colored(f"Got project url {project}, checking status.", "green"))

	req = requests.get(project)
	rpDict = json.loads(req.text)

	if rpDict.get("id") != None:
		print(colored(f"|[Success]|: found project with id {rpDict.get("id")}, name: {rpDict.get("title")}\n", "cyan"))
	else:
		write_to_blacklisted(strId + "\n")
		print(colored(f"|[Error]|: project not found! internal code: {rpDict.get("code")}, status: {req.status_code}\n", "red"))

	return rpDict.get("id")

while True:
	status = check_project()

	if status != None:
		time.sleep(1)
		status = str(status)
		req = requests.post(addProjectUrl + status, headers={"X-Token": token})

		rpDict = json.loads(req.text)

		if rpDict.get("projectId") != None:
			print(colored(f"|[Success]|: added project with id {status} into the studio!\n", "cyan"))
			write_to_blacklisted(status + "\n")
		else:
			print(colored(f"|[Error]|: something went wrong! status code: {req.status_code}, internal response: {req.text}\n", "red"))

	time.sleep(3)
