import signature


@signature.signature
def start(x, y:str,q=2):
	print("first function")

@signature.signature
def start(x, y:int=0, z=3):
	print("second function")

@signature.signature
def start(x, y:int):
	print("second function")

start(3,"hey") #"first function"
start(3,0,3) #"second function"