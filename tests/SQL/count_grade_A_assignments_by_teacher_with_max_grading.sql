-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

-- Common Table Expression (CTE) to calculate the count of grade A assignments for each teacher
WITH GradeACountByTeacher AS (
    SELECT
        teacher_id,
        COUNT(*) AS grade_a_count
    FROM
        assignments
    WHERE
        grade = 'A'
    GROUP BY
        teacher_id
)

-- Query to find the teacher with the maximum grade A assignments
SELECT
    teacher_id,
    grade_a_count
FROM
    GradeACountByTeacher
ORDER BY
    grade_a_count DESC
LIMIT 1;
