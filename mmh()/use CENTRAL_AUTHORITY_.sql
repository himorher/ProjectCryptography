use CENTRAL_AUTHORITY;
CREATE TABLE LOGIN
(
    USER_NAME VARCHAR(40),
    PASSWORD VARCHAR(40),
    PRIMARY KEY (USER_NAME)
);
CREATE TABLE AUTHORITIES
(
    ID CHAR(5),
    AUTHORITIES VARCHAR(40),
    PRIMARY KEY (GID)
);