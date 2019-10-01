import csv
import random
import getCitizen as ctz

with open('citizens.csv', encoding='utf-8', newline='') as file:
    reader = csv.reader(file)
    rows = list(reader)

# Convert phone number into an element, that we will search
def convertNumber(number):
    key = ''
    for v in number.split(')')[1].split('-'):
        key += v
    return int(key)

# To get some info about random citizen in JSON format
def getRandomCitizen():
    index = random.randint(1,len(rows)-1)
    return {
        'index': index,
        'info' : rows[index]
    }

# Show citizen's index, name, phone number and element
def showCitizen(index):
    print("-------")
    print("rows[{}]".format(index))
    print(rows[index][0])
    print(rows[index][1])
    print(convertNumber(rows[index][1]))
    print("-------")

if __name__ == '__main__':
    citizen = getRandomCitizen()
    index = citizen['index']
    person = citizen['info'][0]
    number = citizen['info'][1]
    showCitizen(index)
    ctz.binarySearchWithoutRecursion(rows, convertNumber(number))