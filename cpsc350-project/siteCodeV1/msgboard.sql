DROP DATABASE IF EXISTS siteinfo;
CREATE DATABASE  siteinfo;
\c siteinfo;
DROP TABLE IF EXISTS messageboard;
CREATE TABLE messageboard (
  id serial NOT NULL,
  name varchar(35)  NOT NULL default '',
  day date NOT NULL, 
  age int NOT NULL default 0, 
  message varchar(100) NOT NULL default '');

/* INSERT INTO messageboard (name, day, age, message) VALUES ('Daniel Adams', '2017-01-24', 21, 'I am the creator of this site!');
INSERT INTO messageboard (name, day, age, message) VALUES ('Ashley Otto', '2017-01-26', 22, 'I love this site!');
INSERT INTO messageboard (name, day, age, message) VALUES ('George Washington', '2017-01-27', 285, 'I was the first President of the United States of America.');
INSERT INTO messageboard (name, day, age, message) VALUES ('Benjamin Franklin', '2017-01-27', 311, 'I was never a President, but I am on the $100 bill!');
INSERT INTO messageboard (name, day, age, message) VALUES ('Abraham Lincoln', '2017-01-28', 208, 'I was probably the tallest President of the United States.');
INSERT INTO messageboard (name, day, age, message) VALUES ('Donald Trump', '2017-01-28', 70, 'I am the current President of the United States of America.');
*/