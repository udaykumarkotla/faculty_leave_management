SET foreign_key_checks='ON';
SET sql_safe_updates=0;

create database faculty;
use faculty;
show tables;
drop database faculty;


create table admins(
id varchar(15),
email varchar(50) unique,
username varchar(25) unique,
password1 varchar(20) default 'anits',
password2 varchar(20) default 'admin'
);

create table credentials(
id varchar(15),
email varchar(50) unique,
username varchar(25) unique,
password varchar(20) default 'anits',
password1 varchar(20)
);

SELECT * from credentials;

create table basic(
digit integer primary key auto_increment,
fname varchar(20),
lname varchar(20),
dept varchar(6),
type varchar(15),
designation varchar(20),
mobile varchar(12)
);

create table staff(
id varchar(20) primary key,
email varchar(50) unique,
username varchar(25) unique,
fname varchar(20),
lname varchar(20),
dept varchar(6),
type varchar(15),
designation varchar(20),
mobile varchar(12)
);
 
delimiter $$
create trigger detail after insert on basic
for each row 
begin
insert into staff (id,email,username,fname,lname ,dept ,type ,designation ,mobile) values ((select concat(new.dept,new.digit)),(select concat(new.fname,new.lname,new.digit,'@anits.edu.in')),(select concat(new.fname,new.digit)),new.fname,new.lname,new.dept,new.type,new.designation,new.mobile);
end $$;
delimiter ;

drop trigger detail;

show triggers;

insert into basic values(1001,'Sreekar','teja','CSE','Teaching','Professor','9876543210');
insert into basic (fname,lname ,dept ,type ,designation ,mobile) values('Uday','Kumar','CSE','Teaching','Professor','8774541013');
insert into basic (fname,lname ,dept ,type ,designation ,mobile) values('Benarji','K','MECH','Teaching','Asst.Professor','6724641099');
insert into basic (fname,lname ,dept ,type ,designation ,mobile) values('Vijay','satvik','IT','Teaching','Professor','9884761021');
insert into basic (fname,lname ,dept ,type ,designation ,mobile) values('Uday','Kumar','CSE','Teaching','Professor','8774541013');


select * from staff;

create table leaves(
id varchar(20) primary key,
username varchar(50) unique,
OD integer default 2,
SL integer default 1,
EL integer default 1,
PL integer default 1
);


delimiter $$
create trigger users after insert on basic
for each row
begin
insert into credentials(id,email,username,password1) values ((select concat(new.dept,new.digit)),(select concat(new.fname,new.lname,new.digit,'@anits.edu.in')),(select concat(new.fname,new.digit)),(select concat(new.lname,'ANITS')));
end$$;
delimiter ;

select * from credentials;

select * from leaves;

delimiter $$
create trigger leav after insert on credentials
for each row
begin
insert into leaves(id,username) values(new.id,new.username);
end $$;
delimiter ;


show tables;


create table applyleave(
id varchar(15),
username varchar(25),
noofdays integer,
fromdate date,
todate date,
type varchar(15),
reason varchar(300)
);

create table HodTable(id varchar(15),
username varchar(25),
noofdays integer,
fromdate date ,
todate date,
type varchar(15),
reason varchar(300),
status varchar(25) default 'Pending'
);

create table PrincipalTable(id varchar(15),
username varchar(25),
noofdays integer,
fromdate date ,
todate date,
type varchar(15),
reason varchar(300),
status varchar(25) default 'Pending'
);

delimiter $$
create trigger tohod after insert on applyleave
for each row 
begin
insert into HodTable (id,username,noofdays,fromdate,todate,type,reason) values(new.id,new.username,new.noofdays,new.fromdate,new.todate,new.type,new.reason);
end $$
delimiter ;

delimiter $$
create trigger toprincipal after update on HodTable
for each row
begin
insert into principaltable (id,username,noofdays,fromdate,todate,type,reason)values(new.id,new.username,new.noofdays,new.fromdate,new.todate,new.type,new.reason);
end $$
delimiter ;

insert into applyleave(id,username,noofdays,fromdate,todate,type,reason) values('CSE1001','Sreekar1001',1,'2021-05-18','2021-05-19','SL','Severe mental tensions');

update HodTable set status='Rejected'where id='CSE1001';

create table accepted(id varchar(15),
username varchar(25),
noofdays integer,
fromdate date ,
todate date,
type varchar(15),
reason varchar(300),
status varchar(25)
);   





desc credentials;


update credentials set password="ANITS" where id='CSE1001' and password='anits';


select * from credentials;



create table al(id varchar(15),
username varchar(25),
noofdays integer,
fromdate date,
todate date,
type varchar(15),
reason varchar(300),
status varchar(30) default 'Pending');



select * from applyleave; 


desc leaves;


select * from credentials;

select * from applyleave;

delete  from applyleave ;
