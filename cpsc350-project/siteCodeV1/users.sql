\c siteinfo

drop table if exists crimes;
create table crimes(
    
    crimeType text,
    criminalNumber int,
    crimeDate date,
    casualties int,
    criminalName text,
    threatLevel text,
    crimeLocation text
    
);

INSERT INTO crimes (crimeType, criminalNumber, crimeDate, casualties, criminalName, threatLevel, crimeLocation) VALUES ('Armed Robbery', 3, '2017-02-14', 1, 'Black Rabbit', 'Medium', 'North America');
INSERT INTO crimes (crimeType, criminalNumber, crimeDate, casualties, criminalName, threatLevel, crimeLocation) VALUES ('Carjacking', 1, '2017-02-14', 0, 'Big Boi', 'Low', 'South America');
INSERT INTO crimes (crimeType, criminalNumber, crimeDate, casualties, criminalName, threatLevel, crimeLocation) VALUES ('Assault', 1, '2017-02-14', 4,'Dave', 'High', 'Africa');
INSERT INTO crimes (crimeType, criminalNumber, crimeDate, casualties, criminalName, threatLevel, crimeLocation) VALUES ('Homicide', 5,  '2017-02-14', 15, 'The Joker', 'Very High', 'North America');
INSERT INTO crimes (crimeType, criminalNumber, crimeDate, casualties, criminalName, threatLevel, crimeLocation) VALUES ('Jaywalking', 1, '2017-02-14', 0, 'Ms. Johnson', 'None', 'Europe');


drop table if exists users;
create table users(
    
    username text,
    password text,
    state text
);

/*insert into users (username, password, state) values ('DMoney', crypt('password', gen_salt('bf')),'Virginia');
