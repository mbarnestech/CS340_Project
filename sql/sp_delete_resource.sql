-- Team Members: Julie Anzaroot and Margaret Barnes
-- Project Title: Neighborhood Lending Library
-- Group 41
-- SP file to delete a resource 


DROP PROCEDURE IF EXISTS sp_delete_resource;
DELIMITER //
CREATE PROCEDURE sp_delete_resource(IN id int)
BEGIN
   -- Delete a Resource
   DELETE FROM Resources
      WHERE resourceID = id;
   -- end the stored procedure

   COMMIT;

END //
DELIMITER ;




