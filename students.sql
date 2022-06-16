CREATE TABLE students (
    id int NOT NULL,
    LastName char(20),
    FirstName char(20),
    dept char(10),
    CONSTRAINT students_PK PRIMARY KEY (id),
    CHECK (dept IN ("CSIE","CIS"))
); 

-- alter table students
-- alter FirstName set  default 'nameless';
-- alter table students
-- alter LastName set default 'nameless';
ALTER TABLE students ADD  fid INT DEFAULT 12345;

INSERT INTO students (id,LastName,FirstName,dept)
VALUES (409856043,'Siu','Tony','CSIE'); 
INSERT INTO students (id,LastName,FirstName,dept)
VALUES (123456788,'broken','iclass','CSIE'); 

CREATE TABLE advisor(
  fid int NOT NULL,
  name char(40),
  CONSTRAINT courses_pk PRIMARY KEY(fid),
  CONSTRAINT courses_fk FOREIGN KEY(fid) REFERENCES student_t(fid)
);

INSERT INTO advisor(fid,name)
VALUES (12345,'MR T');

SELECT 
    students.id,
    students.LastName,
    students.FirstName,
    students.dept,
    advisor.fid,
    advisor.name
  FROM 
    students 
    INNER JOIN advisor ON students.fid = advisor.fid;

DELETE FROM students WHERE students.LastName = 'broken';

UPDATE advisor SET
name = 'chenduenkai' WHERE 
fid = 12345
-- drop table students;
-- drop table advisor;