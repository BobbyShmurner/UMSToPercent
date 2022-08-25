import json
import math
from dataclasses import dataclass

def Lerp (a, b, t):
	return (a * (1.0 - t)) + (b * t);

def InverseLerp(a, b, x):
	return (x - a) / (b - a)

@dataclass
class Unit:
	name: str
	umsScores: list[int]
	rawScores: list[int]

@dataclass
class Subject:
	name: str
	units: list[Unit]

subjectsJson = None
with open("subject_data.json", "r") as file:
	subjectsJson = json.loads(file.read())

subjects = []
for subjectJson in subjectsJson["Subjects"]:
	units = []
	for unitJson in subjectJson["Units"]:
		unit = Unit(
			unitJson["Unit"],
			unitJson["UMS"],
			unitJson["Raw"]
		)

		units.append(unit)

	subject = Subject(
		subjectJson["Name"],
		units
	)
	subjects.append(subject)

lerpTime = InverseLerp(80, 100, 95)
print(math.ceil(Lerp(61, 100, lerpTime)))

print("Subject List:\n")
for i in range(len(subjects)):
	subject = subjects[i]
	print(f"{i + 1}. {subject.name}")

choice = int(input("Please pick a subject: "))
subject = subjects[choice - 1]

print("\nUnit List:\n")
for i in range(len(subject.units)):
	unit = subject.units[i]
	print(f"{i + 1}. {unit.name}")

choice = int(input("Please pick a unit: "))
unit = subject.units[choice - 1]

lowerBoundry = -1
upperBoundry = -1
upperBoundryIndex = -1

userUms = int(input("Please enter your UMS: "))

for i in range(len(unit.umsScores)):
	ums = unit.umsScores[i]

	if userUms <= ums:
		upperBoundry = unit.umsScores[i]
		lowerBoundry = unit.umsScores[i - 1]
		upperBoundryIndex = i

rawLerpTime = InverseLerp(lowerBoundry, upperBoundry, userUms)
rawMark = math.ceil(Lerp(unit.rawScores[upperBoundryIndex - 1], unit.rawScores[upperBoundryIndex], rawLerpTime))
percent = math.ceil(rawMark / unit.rawScores[0] * 100)

print(f"Raw Mark: {rawMark}/{unit.rawScores[0]}, Percent: {percent}")