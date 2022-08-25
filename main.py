import json
import math
from dataclasses import dataclass

UMS_LUT = [1, .8, .73, .67, .6, .5, .4, .3, .2]
GRADE_LUT = ["A", "B", "C*", "C", "D", "E", "F", "G"]

def Lerp (a, b, t):
	return (a * (1.0 - t)) + (b * t);

def InverseLerp(a, b, x):
	return (x - a) / (b - a)

@dataclass
class Unit:
	name: str
	maxUMS: int
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
			unitJson["MaxUMS"],
			unitJson["Raw"]
		)

		units.append(unit)

	subject = Subject(
		subjectJson["Name"],
		units
	)
	subjects.append(subject)

print("Subject List:\n")
for i in range(len(subjects)):
	subject = subjects[i]
	print(f"{i + 1}. {subject.name}")

choice = int(input("Please pick a subject: "))
subject = subjects[choice - 1]

print("\nUnit List:\n")
for i in range(len(subject.units)):
	unit = subject.units[i]
	print(f"{i + 1}. {unit.name} (Max UMS: {unit.maxUMS})")

choice = int(input("Please pick a unit: "))
unit = subject.units[choice - 1]

lowerBoundry = -1
upperBoundry = -1
lowerBoundryIndex = -1
upperBoundryIndex = -1
grade = "?"

userUms = int(input("Please enter your UMS: "))

for i in range(len(UMS_LUT)):
	if (unit.rawScores[i] == -1): continue
	ums = math.ceil(unit.maxUMS * UMS_LUT[i])

	if userUms <= ums: continue
	
	upperBoundry = math.ceil(unit.maxUMS * UMS_LUT[i - 1])
	lowerBoundry = ums
	lowerBoundryIndex = i
	upperBoundryIndex = i - 1

	grade = GRADE_LUT[upperBoundryIndex]

	break

rawLerpTime = InverseLerp(lowerBoundry, upperBoundry, userUms)
rawMark = math.ceil(Lerp(unit.rawScores[lowerBoundryIndex], unit.rawScores[upperBoundryIndex], rawLerpTime))
percent = math.ceil(rawMark / unit.rawScores[0] * 100)

print(f"\nGrade: {grade}, Raw Mark: {rawMark}/{unit.rawScores[0]}, Percent: {percent}")