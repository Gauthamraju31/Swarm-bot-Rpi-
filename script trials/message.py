

class Message:

	def __init__(self, messageId = 0, payLoad = []):

		self.messageId = messageId
		self.payLoad = payLoad
		self.pose = ()
		self.target = ()

	def splitPayload(self):

		decodedData = []
		l = []
		a = selfpayLoad.split('/')
		
		for x in a:
			l.append(eval(x))
		decodedData.append(l)
		
		self.messageId = decodedData[0]
		self.pose = decodedData[1]
		self.target = decodedData[2]


	def getPose(self):

		return self.pose

	def getTarget(self):

		return self.target

	def getID(self):

		return self.messageId

	def getMessageasDict(self):

		D = {}
		d[self.messageId] = [self.pose, self.target]
		return D