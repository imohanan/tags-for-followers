import random

def split_training_test_dev(fileName, trainingPercent, testPercent):
	if trainingPercent + testPercent != 100: raise Exception("Percentages don't sum upto 100")
	with open(fileName, 'r') as data_file:
		lines = data_file.readlines()

	header = lines[0]
	lines = lines[1:]

	trainingCount = trainingPercent * len(lines) / 100

	random_indices = random.sample( range(0, len(lines)), len(lines) )

	trainingLines = random_indices[0:trainingCount]
	testLines = random_indices[trainingCount+ 1: ]
	
	with open('data/training.csv', 'w') as training_file:
		training_file.write(header)
	with open('data/training.csv', 'a') as training_file:
		for index in trainingLines:
			training_file.write(lines[index])
			#training_file.write('\n')

	with open('data/test.csv', 'w') as test_file:
		test_file.write(header)
	with open('data/test.csv', 'a') as test_file:
		for index in testLines:
			test_file.write(lines[index])
			#test_file.write('\n')


if __name__ == '__main__':
	split_training_test_dev('data/features.csv', 70, 30)

