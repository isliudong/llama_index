CREATE OR REPLACE PROCEDURE PRO_INSERT(arg1 in VARCHAR,arg2 in VARCHAR,arg3 in number)AS BEGIN insert into S(sno , cno , grade)values(arg1,arg2, arg3);
END PRO_INSERT;