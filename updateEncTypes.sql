UPDATE encounter e
JOIN location l ON l.location_id = e.location_id
SET e.encounter_type =
  (SELECT et.encounter_type_id
   FROM entity_mapping em, encounter_type et
   WHERE em.entity2_uuid = et.uuid AND em.entity1_uuid = l.uuid)
WHERE encounter_type = 1; // update only records where encounter type = consultation
