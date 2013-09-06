import sys

console = sys.stdout
log = None

def setLog(location):
	open('work/log/'+str(location)+'.log', 'w').close()
	log = open('work/log/'+str(location)+'.log', 'w')

	sys.stdout = log

	return log

def resetLog():
	sys.stdout = console

	return console
