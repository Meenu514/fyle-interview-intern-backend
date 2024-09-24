-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

select COUNT(a.grade)
    from assignments a
    where a.grade = 'A'
    and a.state = 'GRADED'
    and a.teacher_id = (
        select teacher_id
        from assignments
        where state = 'GRADED'
        group by teacher_id
        order by COUNT(*) desc
        limit 1
    );
