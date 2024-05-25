USE CLOUD;
create table CUSTOMER
(
    IDCustomer	char(5),
    Name		varchar(40),
    Gender		varchar(3),
    Birth		datetime,
    PhoneNumber		varchar(12),
    Address		varchar(40),
    PRIMARY KEY (IDCustomer)
);


INSERT INTO CUSTOMER VALUES('CU001', 'Frank Volks', 'M', '2001/10/13', '385-200-7503', 'Oakdale, California(CA)');
INSERT INTO CUSTOMER VALUES('CU002', 'Alice Bell', 'F', '1973/02/20', '605-212-1667', '607 Crest Pkwy, Altamonte, Florida(FL)');
INSERT INTO CUSTOMER VALUES('CU003', 'John Rivers', 'M', '1964/06/26', '808-206-3152', '456 Acorn St, Slidell, Louisiana(LA)');
INSERT INTO CUSTOMER VALUES('CU004', 'Isla Best', 'F', '1954/4/6', '708-206-3221', '700 N 19th St, Canon City, Colorado(CO)');
INSERT INTO CUSTOMER VALUES('CU005', 'Chelsey Thornton', 'M', '2001/10/4', '304-224-4734', '331 Main St Catskill, New York(NY)');
INSERT INTO CUSTOMER VALUES('CU006', 'Aleesha Garrett', 'F', '1971/05/15', '208-202-4467', 'Po Box 1 El Dorado, Kansas(KS')
INSERT INTO CUSTOMER VALUES('CU007', 'Callie White', 'F', '1981/05/22', '239-205-8205', '251 Private 5991 Rd');
INSERT INTO CUSTOMER VALUES('CU008', 'Margaret Glenn', 'F', '1999/06/18', '385-201-4425', 'Yantis, Texas(TX)');
INSERT INTO CUSTOMER VALUES('CU009', 'Ella-Louise Steele', 'F', '1970/11/14', '209-230-4906', '731 E Nora Ave Spokane, Washington(WA)');
INSERT INTO CUSTOMER VALUES('CU010', 'Salman Garrison', 'M', '1961/2/10', '208-202-4467', '425 S 3rd St Lindsborg, Kansas(KS)');
INSERT INTO CUSTOMER VALUES('CU011', 'Shakira Bauer', 'F', '1991/10/3', '605-232-0381', '607 Crest Pkwy, Altamonte, Florida(FL)');
INSERT INTO CUSTOMER VALUES('CU012', 'Mikey Rubio', 'M', '1998/2/7', '239-204-7856', '456 Acorn St')
INSERT INTO CUSTOMER VALUES('CU013', 'Rahim Mckenzie', 'M', '1997/12/8', '304-224-4734', 'Slidell, Louisiana(LA)');
INSERT INTO CUSTOMER VALUES('CU014', 'Alannah Taylor', 'F', '2000/01/22', '239-205-8205', '251 Fm 1953, Groesbeck, Texas(TX)');
INSERT INTO CUSTOMER VALUES('CU015', 'Abdullahi Norris', 'M', '2003/01/31', '208-202-4467', 'Baxter Springs, Kansas(KS)');
