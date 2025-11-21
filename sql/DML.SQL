-- Team Members: Julie Anzaroot and Margaret Barnes
-- Project Title: Neighborhood Lending Library
-- Group 41
-- DML file for CRUD operations


-- Select all users
SELECT
   userID,
   firstName as 'First Name',
   lastName as 'Last Name',
   email as Email,
   phone as 'Phone Number'
FROM Users;


-- Select all resources
SELECT
   r.resourceID,
   r.resourceName as Name,
   r.resourceDescription as Description,
   u.firstName as 'Owner First Name',
   u.lastName as 'Owner Last Name'
FROM Resources r
JOIN Users u on r.userID = u.userID ;


-- Search for a resource
SELECT
   r.resourceID,
   r.resourceName as Name,
   r.resourceDescription as Description,
   u.firstName as 'Owner First Name',
   u.lastName as 'Owner Last Name'
FROM Resources r
JOIN Users u on r.userID = u.userID
   WHERE r.resourceName = @resourceName
   OR r.resourceDescription ILIKE %@resourceDescription%;


-- Add a resource
INSERT INTO Resources (userID, resourceName, resourceDescription)
VALUES(
   userID = @userID,
   resourceName = @ resourceName,
   resourceDescription = @ resourceDescription
);


-- Select current active loans by user
SELECT
   l.loanID,
   l.startDate as 'Start Date',
   l.dueDate as 'Due Date',
   r.resourceName as 'Resource Name',
   u.firstName as 'Lender First Name',
   u.lasttName as 'Lender Last Name'
FROM Loans l
JOIN Users u on l.userID = u.userID
JOIN Resources r on l.resourceID = r.resourceID
   WHERE l.returnedDate = NULL
   AND l.userID =
       (SELECT userID
       FROM Users
       WHERE email = @email
       );


-- Select all loans
SELECT
   l.loanID,
   l.startDate as 'Start Date',
   l.dueDate as 'Due Date',
   r.resourceName as 'Resource Name',
   u.firstName as 'Lender First Name',
   u.lasttName as 'Lender Last Name'
FROM Loans l
JOIN Users u on l.userID = u.userID
JOIN Resources r on l.resourceID = r.resourceID;


-- Search Locations
SELECT
   locationID,
   locationName,
   locationDescription
FROM Locations
   WHERE locationDescription ILIKE %@locationDescription%;


-- Select all locations
SELECT
   locationID,
   locationName,
   locationDescription
FROM Locations;


-- Select all ResourceLocation
SELECT
   rl.ResourceLocationsID,
   r.resourceName,
   l.locationName
FROM ResourceLocations rl
JOIN Resources r on rl.resourceID = r.resourceID
JOIN Locations l on rl.locationID = l.locationID;


-- Insert a ResourceLocation
INSERT INTO ResourceLocations (resourceID, locationID)
VALUES(
   (SELECT resourceID FROM Resources WHERE resourceID = @resourceID),
   (SELECT locationID FROM Locations WHERE locationID = @locationID)
);


-- Update a ResourceLocation's locationID
UPDATE ResourceLocations
SET
locationID = (SELECT locationID FROM Locations WHERE locationID = @locationID)
WHERE
  ResourceLocationsID =   @ResourceLocationsID;


-- Delete a ResourceLocation
DELETE FROM ResourceLocations
WHERE
  resourceID =  (SELECT resourceID FROM Resources WHERE resourceDescription = @resourceDescription)
  AND locationID =  (SELECT locationID FROM Locations WHERE locationName = @locationName);


-- Delete a Resource
DELETE FROM Resources
   WHERE resourceID = @resourceID
    
-- Update a Resource Description
UPDATE Resources
SET resourceDescription = @resourceDescription
WHERE resourceID = @resourceID


-- Update a Resource Name
UPDATE Resources
SET resourceName = @resourceName
WHERE resourceID = @resourceID