import sys
import time

PROF_A = 0
PROF_B = 1
PROF_C = 2
PROF_D = 3
PROF_E = 4
PROF_F = 5

LECTURE_1 = 0
LECTURE_2 = 1
LECTURE_3 = 2
LECTURE_4 = 3
LECTURE_5 = 4
LECTURE_6 = 5

PREFERENCES = {
	PROF_A: { LECTURE_2: 1, LECTURE_3: 2, LECTURE_4: 3, LECTURE_5: 4, LECTURE_6: 5 },
	PROF_B: { LECTURE_1: 1, LECTURE_3: 2, LECTURE_4: 3, LECTURE_5: 4, LECTURE_6: 5 },
	PROF_C: { LECTURE_1: 1, LECTURE_2: 2, LECTURE_4: 3, LECTURE_5: 4, LECTURE_6: 5 },
	PROF_D: { LECTURE_1: 1, LECTURE_2: 2, LECTURE_4: 3, LECTURE_5: 4, LECTURE_6: 5 },
	PROF_E: { LECTURE_1: 1, LECTURE_2: 2, LECTURE_3: 3, LECTURE_4: 4, LECTURE_6: 5 },
	PROF_F: { LECTURE_1: 1, LECTURE_2: 2, LECTURE_3: 3, LECTURE_4: 4, LECTURE_5: 5 },
}

DOUBLE_BOOK_PENALTY = 1000


def check_double_booking(occupied_list, prof):
	if prof in occupied_list:
		return DOUBLE_BOOK_PENALTY
	occupied_list.add(prof)
	return 0


def get_pref(prof, lecture_id):
	prefs = PREFERENCES[prof]
	if lecture_id not in prefs:
		print "Professor %i has no preference for lecture %i" % (prof, lecture_id)
		return DOUBLE_BOOK_PENALTY
	return prefs[lecture_id]


class Lecture(object):
	def __init__(self, id, host, guests):
		self._id = id
		self._host = host
		self._guests = guests

	def calculate_score(self, occupied_profs):
		score = 0
		score += check_double_booking(occupied_profs, self._host)
		for guest in self._guests:
			score += get_pref(guest, self._id)
			score += check_double_booking(occupied_profs, guest)
		return score


class Schedule(object):
	def __init__(self, lectures):
		self._lectures = lectures

	def calculate_score(self):
		score = 0
		for l1, l2 in self._lectures:
			occupied_profs = set()
			score += l1.calculate_score(occupied_profs)
			score += l2.calculate_score(occupied_profs)
		return score


schedule = Schedule([
	[ Lecture(LECTURE_1, PROF_A, [PROF_B, PROF_C]), Lecture(LECTURE_4, PROF_D, [PROF_E, PROF_F]) ],
	[ Lecture(LECTURE_2, PROF_B, [PROF_A, PROF_C]), Lecture(LECTURE_5, PROF_E, [PROF_D, PROF_F]) ],
	[ Lecture(LECTURE_3, PROF_C, [PROF_A, PROF_B]), Lecture(LECTURE_6, PROF_F, [PROF_D, PROF_E]) ],
])

LOOPS = 1000000
best_score = sys.maxint
start = time.time()
for x in range(0, LOOPS):
	score = schedule.calculate_score()
	best_score = min(score, best_score)
end = time.time()

total_time = end - start
print "Calcuated %i scores in %f seconds (%f per score)" % (LOOPS, total_time, total_time / LOOPS)
print "Best Score: %i" % (best_score)
