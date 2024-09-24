-- Write query to get number of graded assignments for each student:


select a.student_id as ID, count(state) as assignments from assignments as a
	where state='GRADED'
    group by a.student_id;