-- Team Members: Julie Anzaroot and Margaret Barnes
-- Project Title: Neighborhood Lending Library
-- Group 41
-- SP file to delete a resource location

DROP PROCEDURE IF EXISTS sp_delete_resourceLocation;
DELIMITER //
CREATE PROCEDURE sp_delete_resourceLocation(IN id int)
BEGIN
    -- Delete a ResourceLocation
    DELETE FROM ResourceLocations
    WHERE resourceLocationsID = id;
    -- end the stored procedure
    
    COMMIT;
END //
DELIMITER ;