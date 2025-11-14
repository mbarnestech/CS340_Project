-- Team Members: Julie Anzaroot and Margaret Barnes
-- Project Title: Neighborhood Lending Library
-- Group 41
-- DLL file to create the database and add example data


SET FOREIGN_KEY_CHECKS=0;
SET UNIQUE_CHECKS=0;
SET AUTOCOMMIT = 0;


DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Resources;
DROP TABLE IF EXISTS Loans;
DROP TABLE IF EXISTS Locations;
DROP TABLE IF EXISTS ResourceLocations;


-- Create Queries


-- Users table records the details of Users of the Neighborhood Lending Library.
CREATE TABLE Users (
   userID INT AUTO_INCREMENT NOT NULL,
   firstName VARCHAR(25) NOT NULL ,
   lastName VARCHAR(45) NOT NULL,
   email VARCHAR(254) NOT NULL UNIQUE,
   phone VARCHAR(20) UNIQUE,
   PRIMARY KEY (userID)
);


-- Resources table records the details of the Resources submitted.
CREATE TABLE Resources (
   resourceID  INT AUTO_INCREMENT NOT NULL,
   userID  INT NOT NULL,
   resourceName VARCHAR(100) NOT NULL ,
   resourceDescription VARCHAR(300) NOT NULL UNIQUE,
   FOREIGN KEY (userID) REFERENCES Users(userID)
       ON DELETE CASCADE,
   PRIMARY KEY (resourceID)
);


-- Loans table records current and previous Loans.
CREATE TABLE Loans (
   loanID  INT AUTO_INCREMENT NOT NULL,
   startDate DATE NOT NULL,
   dueDate DATE NOT NULL,
   returnedDate DATE,
   userID  INT,
   resourceID INT,
   FOREIGN KEY (userID) REFERENCES Users(userID)
       ON DELETE SET NULL,
   FOREIGN KEY (resourceID) REFERENCES Resources(resourceID)
       ON DELETE SET NULL,
   PRIMARY KEY (loanID)
);




-- Locations table records the details of the Locations a specific resource is available to be collected from.
-- This is a meeting point between the owner and the borrower and there may be more than one possible meeting point.
CREATE TABLE Locations (
   locationID  INT AUTO_INCREMENT NOT NULL,
   locationName VARCHAR(100) UNIQUE,
   locationDescription VARCHAR(300),
   PRIMARY KEY (locationID)
);


-- ResourceLocations table is an intersection table to link the M:M relationship
-- between Resources and Locations.
CREATE TABLE ResourceLocations (
   resourceLocationsID INT AUTO_INCREMENT NOT NULL,
   resourceID  INT NOT NULL,
   locationID  INT NOT NULL,
   FOREIGN KEY (resourceID) REFERENCES Resources(resourceID)
       ON DELETE CASCADE,
   FOREIGN KEY (locationID) REFERENCES Locations(locationID)
       ON DELETE CASCADE,
   CONSTRAINT uniqueResourceLocation UNIQUE (resourceID, locationID),
   PRIMARY KEY (resourceLocationsID)
);


-- Insert Queries
-- chatGPT was used to generate the names, emails and phone numbers
-- with the following prompt: `provide 3 examples with the following data: firstName, lastName, email, us phone`
INSERT INTO Users (firstName, lastName, email, phone)
VALUES ('Alice', 'Johnson', 'alice.johnson@example.com', '555-123-4567'),
('Bob', 'Smith', 'bob.smith@example.com', '555-234-5678'),
('Charlie', 'Davis', 'charlie.davis@example.com', '555-345-6789');


INSERT INTO Resources (userID, resourceName, resourceDescription)
VALUES((SELECT userID FROM Users WHERE email = 'alice.johnson@example.com'), 'ladder', 'sturdy 6 foot aluminium folding ladder'),
((SELECT userID FROM Users WHERE email = 'bob.smith@example.com'), 'book', 'hard cover first book of Harry Potter series, Harry Potter and the  Sorcerer''s Stone'),
((SELECT userID FROM Users WHERE email = 'bob.smith@example.com'), 'curling iron', 'Curl X Ceramic curling iron');


-- chatGPT was used to generate the locations and location descriptions
-- with the following prompt: `3 made up locations and location descriptions - like directions, for potential neighborhood meeting points`
INSERT INTO Locations (locationName, locationDescription)
VALUES('Sunnybrook Corner', 'Head down Sunnybrook Drive until you reach the small park at the end. The meeting spot is by the wooden bench, just across from the basketball court.'),
('Lakeside Steps', 'Walk toward the end of Harbor Lane and follow the path along the water. The meeting point is at the stone steps overlooking the lake, near the blue boathouse.'),
('Pineview Circle', 'Go past the community garden on Pineview Road and take the second left into Pineview Circle. Meet by the round flower bed in the center — next to the lamp post with the green sign.');




INSERT INTO Loans (startDate, dueDate, returnedDate, userID, resourceID)
VALUES('2025-10-01', '2025-10-15', '2025-10-14',(SELECT userID FROM Users WHERE email = 'charlie.davis@example.com'), (SELECT resourceID FROM Resources WHERE resourceDescription = 'sturdy 6 foot aluminium folding ladder')),
('2025-10-20', '2025-10-30', NULL,(SELECT userID FROM Users WHERE email = 'alice.johnson@example.com'), (SELECT resourceID FROM Resources WHERE resourceDescription = 'Curl X Ceramic curling iron')),
('2025-10-10', '2025-11-10', NULL, (SELECT userID FROM Users WHERE email ='charlie.davis@example.com'), (SELECT resourceID FROM Resources WHERE resourceDescription = 'hard cover first book of Harry Potter series, Harry Potter and the  Sorcerer''s Stone'));




INSERT INTO ResourceLocations (resourceID, locationID)
VALUES((SELECT resourceID FROM Resources WHERE resourceDescription = 'sturdy 6 foot aluminium folding ladder'),(SELECT locationID FROM Locations WHERE locationName = 'Sunnybrook Corner')),
((SELECT resourceID FROM Resources WHERE resourceDescription = 'hard cover first book of Harry Potter series, Harry Potter and the  Sorcerer''s Stone'),(SELECT locationID FROM Locations WHERE locationName = 'Sunnybrook Corner')),
((SELECT resourceID FROM Resources WHERE resourceDescription = 'hard cover first book of Harry Potter series, Harry Potter and the  Sorcerer''s Stone'),(SELECT locationID FROM Locations WHERE locationName = 'Lakeside Steps')),
((SELECT resourceID FROM Resources WHERE resourceDescription = 'hard cover first book of Harry Potter series, Harry Potter and the  Sorcerer''s Stone'),(SELECT locationID FROM Locations WHERE locationName = 'Pineview Circle')),
((SELECT resourceID FROM Resources WHERE resourceDescription = 'Curl X Ceramic curling iron'),(SELECT locationID FROM Locations WHERE locationName = 'Lakeside Steps')),
((SELECT resourceID FROM Resources WHERE resourceDescription = 'Curl X Ceramic curling iron'),(SELECT locationID FROM Locations WHERE locationName = 'Pineview Circle'));




SET FOREIGN_KEY_CHECKS=1;
SET UNIQUE_CHECKS=1;
COMMIT;