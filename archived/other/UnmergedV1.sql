CREATE TABLE People (
	people_id INT NOT NULL AUTO_INCREMENT,
    	origin_database TINYTEXT NOT NULL,
    	email TINYTEXT,
    	phone BIGINT(20),
    	name TEXT,
	first_name TINYTEXT,
	middle_name TINYTEXT,
	last_name TINYTEXT,
	nih_id BIGINT(20),
    	PRIMARY KEY (people_id)
);


CREATE TABLE PeopleAliasID (
	people_id INT NOT NULL,
	alias_id INT NOT NULL,

    FOREIGN KEY (people_id)
      	REFERENCES People(people_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE Org (
	org_id INT NOT NULL AUTO_INCREMENT,
	origin_database TINYTEXT NOT NULL,
	name TEXT NOT NULL,
	PRIMARY KEY (org_id)
);


CREATE TABLE OrgAliasID (
	org_id INT NOT NULL,
	alias_id INT NOT NULL,

	FOREIGN KEY (org_id)
      	REFERENCES Org(org_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE PeopleOrg (
	people_id INT NOT NULL,
	org_id INT NOT NULL,
	year YEAR,
	relation_strength DECIMAL,

    FOREIGN KEY (people_id)
      	REFERENCES People(people_id)
      	ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (org_id)
      	REFERENCES Org(org_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE Project (
	project_id INT NOT NULL AUTO_INCREMENT,
	origin_database TINYTEXT NOT NULL,
	title TEXT NOT NULL,
	PRIMARY KEY (project_id)
);


CREATE TABLE Publication (
	pub_id INT NOT NULL AUTO_INCREMENT,
	origin_database TINYTEXT NOT NULL,
	title TEXT NOT NULL,
	PRIMARY KEY (pub_id)
);


CREATE TABLE Work (
	work_id INT NOT NULL AUTO_INCREMENT,
	project_id INT,
	pub_id INT,
	PRIMARY KEY (work_id),

    FOREIGN KEY (project_id)
      	REFERENCES Project(project_id)
      	ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (pub_id)
      	REFERENCES Publication(pub_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE ProjectAliasID (
	project_id INT NOT NULL,
	alias_id INT NOT NULL,

    FOREIGN KEY (project_id)
      	REFERENCES Project(project_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE PubAliasID (
	pub_id INT NOT NULL,
	alias_id INT NOT NULL,

    FOREIGN KEY (pub_id)
      	REFERENCES Publication(pub_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE Bioentity (
	bio_id INT NOT NULL AUTO_INCREMENT,
	origin_database TINYTEXT NOT NULL,
	name TEXT NOT NULL,
	PRIMARY KEY (bio_id)
);


CREATE TABLE Keyword (
	work_id INT NOT NULL,
	bio_id INT NOT NULL,

    FOREIGN KEY (work_id)
      	REFERENCES Work(work_id)
      	ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (bio_id)
      	REFERENCES Bioentity(bio_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE Source (
	work_id INT NOT NULL,
	source TEXT NOT NULL,

    FOREIGN KEY (work_id)
      	REFERENCES Work(work_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE WorkPeople (
	work_id INT NOT NULL,
	people_id INT NOT NULL,

    FOREIGN KEY (work_id)
      	REFERENCES Work(work_id)
      	ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (people_id)
      	REFERENCES People(people_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE WorkOrg (
	work_id INT NOT NULL,
	org_id INT NOT NULL,

    FOREIGN KEY (work_id)
      	REFERENCES Work(work_id)
      	ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (org_id)
      	REFERENCES Org(org_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


ALTER TABLE Org ADD funding DECIMAL;


CREATE TABLE OrgRelation (
	org_id1 INT NOT NULL,
	org_id2 INT NOT NULL,
	relation ENUM('parent', 'child'),

FOREIGN KEY (org_id1)
      	REFERENCES Org(org_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE PeopleSpec (
	people_id INT NOT NULL,
	bio_id INT NOT NULL,

    FOREIGN KEY (people_id)
      	REFERENCES People(people_id)
      	ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (bio_id)
      	REFERENCES Bioentity(bio_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE BioRelation (
	bio_id1 INT NOT NULL,
	bio_id2 INT NOT NULL,
	relation ENUM('parent', 'child'),

    FOREIGN KEY (bio_id1)
      	REFERENCES Bioentity(bio_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


ALTER TABLE PeopleOrg DROP COLUMN relation_strength;
ALTER TABLE Project ADD start_date DATE;
ALTER TABLE Publication ADD pmid INT;
ALTER TABLE Publication DROP COLUMN title;
ALTER TABLE Publication ADD COLUMN title TEXT NULL;


CREATE TABLE ProjectPub (
	project_id INT NOT NULL,
	pub_id INT NOT NULL,

	FOREIGN KEY (project_id)
		REFERENCES Project(project_id)
		ON UPDATE CASCADE ON DELETE CASCADE,

	FOREIGN KEY (pub_id)
		REFERENCES Publication(pub_id)
		ON UPDATE CASCADE ON DELETE CASCADE
);


DROP TABLE Source;
DROP TABLE WorkOrg;
DROP TABLE WorkPeople;
DROP TABLE ProjectPub;
DROP TABLE ProjectAliasID;
DROP TABLE PubAliasID;
DROP TABLE Keyword;
DROP TABLE Work;
DROP TABLE Project;
DROP TABLE Publication;


CREATE TABLE Work (
    work_id INT NOT NULL,
    origin_database TINYTEXT NOT NULL,
    title TEXT,
    start_date DATE,
    end_date DATE,
    type TINYTEXT NOT NULL,
    pmid INT,

    PRIMARY KEY (work_id)
);


CREATE TABLE WorkRelation (
    work_id1 INT NOT NULL,
    work_id2 INT NOT NULL,
    relation TINYTEXT NOT NULL,

    FOREIGN KEY (work_id1)
		REFERENCES Work(work_id)
		ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE WorkPeople (
	work_id INT NOT NULL,
	people_id INT NOT NULL,

    FOREIGN KEY (work_id)
      	REFERENCES Work(work_id)
      	ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (people_id)
      	REFERENCES People(people_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE WorkOrg (
	work_id INT NOT NULL,
	org_id INT NOT NULL,

    FOREIGN KEY (work_id)
      	REFERENCES Work(work_id)
      	ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (org_id)
      	REFERENCES Org(org_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE Keyword (
	work_id INT NOT NULL,
	bio_id INT NOT NULL,

    FOREIGN KEY (work_id)
      	REFERENCES Work(work_id)
      	ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (bio_id)
      	REFERENCES Bioentity(bio_id)
      	ON UPDATE CASCADE ON DELETE CASCADE
);
