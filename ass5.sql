-- 5-38 a,b
CREATE TABLE student_tb (
    student_id int,
    student_name text,
     CONSTRAINT pk_1 PRIMARY KEY (student_id)
 );

INSERT INTO student_tb (student_id,student_name)
VALUES (38214,'Letersky'); 

INSERT INTO student_tb (student_id,student_name)
VALUES (54907,'Altvater'); 

INSERT INTO student_tb (student_id,student_name)
VALUES (66324,'Aiken');

INSERT INTO student_tb (student_id,student_name)
VALUES (70542,'Marra');

--a
ALTER TABLE student_tb
ADD class char(100);

CREATE TABLE registration_tb(
    test1 int,
    test2 int,
    CONSTRAINT pk_1 PRIMARY KEY(test1)
);

--b
DROP TABLE registration_tb;

INSERT INTO student_tb (class)
VALUES ('ISM 4212');

-- 5-39 
--a
INSERT INTO student_tb (student_id,student_name)
VALUES (65798,'Lopez');

INSERT INTO student_tb 
VALUES (65798,'Lopez');

--b
DELETE FROM student_tb WHERE student_tb.student_id = 65798;

--c
DELETE FROM student_tb WHERE student_tb.student_name LIKE '%Lopez%';

--d
UPDATE student_tb
SET class = 'Introduction to Relational Databases'
WHERE class LIKE '%ISM%'; 

-- 5-40 

--a
SELECT * FROM student_tb 
WHERE student_id < 50000;

--b
DROP TABLE faculty_tb;

CREATE TABLE fac_tb (
    fac_id int,
    fac_name VARCHAR(30),
    CONSTRAINT pk_1 PRIMARY KEY (fac_id)
);

INSERT INTO fac_tb (fac_id,fac_name)
VALUES (4756,'name');

SELECT fac_name
FROM fac_tb
WHERE fac_id = 4756;

--c
CREATE TABLE sec_tb(
    section_no int,
    Semester VARCHAR(30),
    course_id VARCHAR(30),
    CONSTRAINT pk_1 PRIMARY KEY (section_no)
);
INSERT INTO sec_tb (section_no,Semester,course_id)
VALUES (2712,'I-2018','ISM 3113');

INSERT INTO sec_tb (section_no,Semester,course_id)
VALUES (2713,'I-2018','ISM 3113');

INSERT INTO sec_tb (section_no,Semester,course_id)
VALUES (2714,'I-2018','ISM 4212');

INSERT INTO sec_tb (section_no,Semester,course_id)
VALUES (2715,'I-2018','ISM 4930');

SELECT min(section_no )
FROM sec_tb;

-- 6-25 Write an SQL query to answer the following question: 
-- which instructors are qualified to teach ISM 3113?

CREATE TABLE qualified_tb (
    faculty_id int,
    course_id char(30),
    data_qualified char(30) 
--     constraint pk primary key (faculty_id)
);
-- drop table qualified_tb;
INSERT INTO qualified_tb (faculty_id,course_id,data_qualified)
VALUES (2143,'ISM 3112','9/2008');
INSERT INTO qualified_tb (faculty_id,course_id,data_qualified)
VALUES (2143,'ISM 3113','9/2008');
INSERT INTO qualified_tb (faculty_id,course_id,data_qualified)
VALUES (3467,'ISM 4212','9/2015');
INSERT INTO qualified_tb (faculty_id,course_id,data_qualified)
VALUES (3467,'ISM 4930','9/2011');
INSERT INTO qualified_tb (faculty_id,course_id,data_qualified)
VALUES (4756,'ISM 3113','9/2011');
INSERT INTO qualified_tb (faculty_id,course_id,data_qualified)
VALUES (4756,'ISM 3112','9/2011');

CREATE TABLE faculty_tb(
    faculty_id int,
    faculty_name char(30),
    CONSTRAINT pk PRIMARY KEY (faculty_id)
);
INSERT INTO faculty_tb (faculty_id,faculty_name)
VALUES (2143,'Birkin');
INSERT INTO faculty_tb (faculty_id,faculty_name)
VALUES (3467,'Berndt');
INSERT INTO faculty_tb (faculty_id,faculty_name)
VALUES (4756,'Collins');

SELECT faculty_name
FROM faculty_tb ,qualified_tb 
--(select faculty_name,faculty_id from faculty_tb),(select course_id as 'id' from qualified_tb where course_id = 'ISM 3113') --practice
WHERE faculty_tb.faculty_id = qualified_tb.faculty_id
    AND qualified_tb.course_id = 'ISM 3113';

-- 6-26 a,b,c

CREATE TABLE course_tb(
    course_id char(30),
    course_name char(30)
);

INSERT INTO course_tb (course_id,course_name)
VALUES ('ISM 3113','Syst Analysis');
INSERT INTO course_tb (course_id,course_name)
VALUES ('ISM 3112','Syst Design');
INSERT INTO course_tb (course_id,course_name)
VALUES ('ISM 4212','Database');
INSERT INTO course_tb (course_id,course_name)
VALUES ('ISM 4930','Networking');

-- a
SELECT *
FROM course_tb
WHERE course_id LIKE 'ISM%';

--b
INSERT INTO sec_tb (section_no,Semester,course_id)
VALUES (2712,'I-2018','ISM 3113');
INSERT INTO sec_tb (section_no,Semester,course_id)
VALUES (2713,'I-2018','ISM 3113');
INSERT INTO sec_tb (section_no,Semester,course_id)
VALUES (2714,'I-2018','ISM 4212');
INSERT INTO sec_tb (section_no,Semester,course_id)
VALUES (2715,'I-2018','ISM 4930');

SELECT c.course_name,s.section_no,q.course_id 
FROM faculty_tb AS f,course_tb AS c, sec_tb AS s,qualified_tb AS q
    WHERE f.faculty_name = 'Berndt'
        AND f.faculty_id = q.faculty_id
        AND q.course_id = s.course_id
        AND q.course_id = c.course_id;
        
--c 
CREATE TABLE reg_tb (
    student_id int,
    sec_no int
);

INSERT INTO reg_tb (student_id,sec_no)
VALUES (38214,2714);

INSERT INTO reg_tb (student_id,sec_no)
VALUES (54907,2714);

INSERT INTO reg_tb (student_id,sec_no)
VALUES (54907,2715);

INSERT  INTO reg_tb (student_id,sec_no)
VALUES (66324,2713);

SELECT student_tb.student_id,student_tb.student_name,sec_tb.section_no,sec_tb.course_id
FROM student_tb,sec_tb,reg_tb
WHERE reg_tb.sec_no = sec_tb.section_no
    AND sec_tb.course_id = 'ISM 4212'
    AND student_tb.student_id = reg_tb.student_id;

