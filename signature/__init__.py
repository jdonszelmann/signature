import inspect
names = {}
class signature:
	functions = []
	def __new__(cls,func):
		if func.__name__ not in names:
			o = super().__new__(cls)
			names[func.__name__] = o
			return o
		return names[func.__name__]

	def __init__(self,func):
		l1 = inspect.getfullargspec(func)[3]
		l2 = inspect.getfullargspec(func)[0]
		if l1 == None: l1 = []
		if l2 == None: l2 = []
		kwargs=["{}={}".format(key,repr(item)) for key,item in zip(l2[len(l2)-len(l1):],l1)]
		d = {}
		exec("""def fakefunc({args},{kwargs}): pass""".format(args=",".join(l2[:len(l2)-len(l1)]),kwargs=",".join(kwargs)),d)
		self.functions.append((func,d["fakefunc"]))

	def __call__(self,*args,**kwargs):
		choices = []
		for i in self.functions:
			try:
				i[1](*args,**kwargs)
				choices.append(i)
			except TypeError: pass
		if len(choices) == 1: return choices[0][0](*args,**kwargs)
		total = choices
		for i in total:
			if len(inspect.getfullargspec(i[0])[6]) > 0:
				for name,annotation in inspect.getfullargspec(i[0])[6].items():
					if name in kwargs and type(kwargs[name]) != annotation:
						choices.remove(i)
					elif inspect.getfullargspec(i[0])[0].index(name) < len(args) and type(args[inspect.getfullargspec(i[0])[0].index(name)]) != annotation:
						choices.remove(i)
		if len(choices) == 1: return choices[0][0](*args,**kwargs)