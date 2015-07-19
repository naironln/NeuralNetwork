import math
import re
from random import random, randrange


class Neuron:
	"""
	class responsible for simulating a neuron work
	"""
	def __init__(self, bias, activation_value, activation_function, neuron_id):

		#Exceptions
		if type(bias) is not float and type(bias) is not int:
			raise Exception("Bias type must be float or int")

		if type(activation_value) is not float and type(activation_value) is not int:
			raise Exception("Activation type must be float or int")

		if type(activation_function) is not tuple:
			raise Exception("Activation_function must be a tuple")

		if len(activation_function) != 2:
			raise Exception("Activation_function must have only two values")

		for i in activation_function:
			if i != 0 and i != 1:
				raise Exception("Activation_function itens must be zero or one")

		if type(neuron_id) is not int:
			raise Exception("Neuron_id type must be int")

		#properties
		self.bias 				= bias
		self.activation_value 	= activation_value
		self.stimulus			= bias
		self.id					= "n" + str(neuron_id)
		self.result				= 0

		#0 -> sigmoid
		#	0 -> not hyperbolic
		#	1 -> hyperbolic
		##
		#1 -> threshold
		#	0 -> not signum
		#	1 -> signum
		self.activation_function = activation_function 

	def excite(self, excite):
		"""
			increment stimulus of neuron, then if stimulus > activation_value then neuron will be active
		
			excite > value to be incremented
		"""

		self.stimulus += excite

		if self.stimulus >= self.activation_value:

			self.result = self.activate()
			self.stimulus = 0
			return self.result

	def activate(self):
		"""
			call activation function, seted by self.activation_function
		"""


		if self.activation_function[0] == 0:
			return self.sigmoid(self.activation_function[1])

		else:
			return self.threshold(self.activation_function[1])

	def sigmoid(self,hyperbolic,limit=1,inclination=0.1):
		"""
			activation function of sigmoid type (parabolic),

				hyperbolic 	> type of parable. 1 = hyperbolic, 0 = not hyperbolic
					if hyperbolic, the parable will abrange negative values
				inclination > set inclination of parable
		"""

		excite 			= self.stimulus
		self.stimulus 	= self.bias

		if hyperbolic:
			#return inclination*((math.exp(limit*ativation)-math.exp(-limit*ativation))/(math.exp(limit*ativation)+math.exp(limit*ativation)))
			#ativation = math.radians(ativation)
			return math.tanh(excite)
		else:
			return 1/(1+math.exp(-inclination*excite))

	def threshold(self,signum=0):

		excite 			= self.stimulus
		self.stimulus 	= self.bias

		if signum:
			if excite > 0: return 1
			else: return -1
		else:
			if excite > 0: return 1
			else: return 0

class Weight:
	"""
		set weights between neurons 

		value > set value of the weights (must be float and be between 0 and 1)
		edges > set neurons (can also be input or output) dat this weight connect
	"""

	def __init__(self, value, edges):
		if len(edges) != 2:
			raise Exception("Edges must have only two neurons")

		is_neuron = 0
		for i in edges:
			if type(i) is not str:
				is_neuron += 1
				print i

		if is_neuron >= 2:
			raise Exception("Edges content must be a str")

		if type(edges) is not tuple:
			raise Exception("Edges must be a tuple")

		if type(value) is not float:
			raise Exception("Value type must be a float")

		if value < 0  or value > 1:
			raise Exception("Value must be bigger than zero and smaller than one")

		self.value = value
		self.edges = edges
		self.result= 0
	
	def mult(self, activation_value):
		"""
			multply activation value by weight value
		"""

		self.result = activation_value*self.value
		return self.result

class Input:
	"""
		That class represent inputs of a neural network
	"""
	def __init__(self, name, max_value, input_id):
		if type(name) is not str:
			raise Exception("Name type must be a String")

		if type(max_value) is not float and type(max_value) is not int:
			raise Exception("Max_value type must be a float or int")

		if type(input_id) is not int:
			raise Exception("Input_id type must be int")

		self.name 		= ""
		self.max_value 	= max_value
		self.id 		= "i" + str(input_id)

		self.value 		= None

	def input(self, value):
		if type(value) is not float and type(value) is not int:
			raise Exception("Value type must be a float or int")

		if value > self.max_value:
			raise Exception("Value must be smaller than max_value")	

		self.value = value/self.max_value
		
		return self.value

class Output:
	def __init__(self, name, output_id):
		if type(name) is not str:
			raise Exception("Name type must be a String")

		if type(output_id) is not int:
			raise Exception("output_id type must be int")

		self.name 	 = name
		self.id 	 = "o" + str(output_id)
		self.result	 = 0
		self.desired = 0 

	def output(self, value):		
		if type(value) is not float and type(value) is not int:
			raise Exception("Value type must be a float or int")

		return value

class Neural_network:
	def __init__(self):
		self.layers 	= []
		self.inputs 	= []
		self.outputs 	= []
		self.weights	= []

		self.learn_fee	= 0.1

	def create_input(self, name, max_value=1):
		self.inputs.append(Input(name, max_value, len(self.inputs)))

	def create_output(self, name):
		self.outputs.append(Output(name, len(self.outputs)))

	def create_weight(self, value, edges):
		self.weights.append(Weight(value, edges))

	def create_layer(self):
		self.layers.append([])

	def create_neuron(self, bias, activation, activation_function, layer):
		neuron_id = 0
		for i in self.layers:
			neuron_id += len(i)
		
		self.layers[layer].append(Neuron(bias, activation, activation_function, neuron_id))

	def connect(self):
		for i in self.inputs:
			for neuron in self.layers[0]:
				self.create_weight(random(), (i.id,neuron.id))

		for i in range(len(self.layers)):
			if i == len(self.layers)-1:
				for neuron in self.layers[i]:
					for output in self.outputs:
						self.create_weight(random(),(neuron.id,output.id))
			else:
				for neuron1 in self.layers[i]:
					for neuron2 in self.layers[i+1]:
						self.create_weight(random(),(neuron1.id,neuron2.id))

		for weight in self.weights: print weight.edges[0], weight.value, weight.edges[1]
		

	def get_synapses(self, element_id, position):
		synapse_list = []
		
		for weight in self.weights:
			if weight.edges[position] == element_id:
				synapse_list.append(weight)

		return synapse_list

	def set_input(self, element_id, v):
		text = "Type"+ element_id+ "value:"
		inp  = v #raw_input(text)
		
		for i in self.inputs:
			if i.id == element_id:
				print [element_id, i.input(int(inp))]
				return [element_id, i.input(int(inp))]

	def set_desired_result(self, element_id, v):
		text 	= "type" + element_id + "desired output"
		desired = v#raw_input(text)

		desired_result = []

		for o in self.outputs:
			if o.id == element_id:
				o.desired_result = desired



	def search(self, id):
		id_type = re.match(r'(\w)', id).group()

		if id_type == 'i':
			for i in self.inputs:
				if i.id == id: return i

		if id_type == 'n':
			for layer in self.layers:
				for neuron in layer:
					if neuron.id == id: return neuron
		
		if id_type == 'o':
			for output in self.outputs:
				if output.id == id: return output

		

	def feed_forward(self):
		input_range = [[[1,0],1],[[0,1],1],[[1,1],0],[[0,0],0]]
		inputs 		= input_range[randrange(0, len(input_range))]

		for i in range(len(self.inputs)): self.set_input(self.inputs[i].id, inputs[0][i])

		for o in self.outputs: self.set_desired_result(o.id, inputs[1])

		for i in self.inputs: 
			self.make_synapses(i.id, i.value)

		for layer in self.layers:
			for neuron in layer:
				weights = self.get_synapses(neuron.id, 1)
				stimulus = 0
				
				for weight in weights:
					stimulus += weight.result
		
				if neuron.excite(stimulus):
					synapses = self.get_synapses(neuron.id, 0)
					for weight in synapses:
						weight.mult(neuron.result)

		for out in self.outputs:
			self.get_synapses(out.id, 1)
			value = 0			

			for weight in self.weights: 
				value += weight.result

			out.result = value

			print out.output(value)
			#print self.calc_error(out, value)

	def calc_error(self, output, value): 
		return ((value - output.desired)** 2)*0.5


	def make_synapses(self, element_id, value): 
		for weight in self.get_synapses(element_id, 0):
			weight.mult(value)


	def back_propagation(self):
		for output in self.outputs:
			for weight in self.get_synapses(output.id, 1):
				error = self.calc_error(output, weight.value)

				if weight.value > 0:
					weight.value -= self.learn_fee * (error*weight.value)

				for layer in self.layers:
					element_id  = weight.edges[0]
					
					for weight in self.get_synapses(element_id, 1):
						if weight.value > 0: 
							weight.value -= (self.learn_fee*0.5) * (error*weight.value)







def run():
	nt = Neural_network()

	nt.create_input("entrada1", 1)
	nt.create_input("entrada2", 1)

	nt.create_layer()

	nt.create_neuron(0,1,(0,1),0)
	nt.create_neuron(0,1,(0,1),0)

	nt.create_output("output1")


	nt.connect()
	for weight in nt.weights:
		print weight.value

	for i in range(5000):
		print i
		nt.feed_forward()
		nt.back_propagation()

	for weight in nt.weights:
		print weight.value

#run()



