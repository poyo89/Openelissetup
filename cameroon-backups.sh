#!/bin/bash
BACKUP_PATH="/opt/backups"
mkdir -p $BACKUP_PATH
TIME=`date +%Y%m%d_%H%M%S`
service openmrs stop
service bahmni-reports stop
service bahmni-lab stop
service odoo stop
mysqldump -uroot -ppassword openmrs > $BACKUP_PATH/openmrs_$TIME.sql
mysqldump -uroot -ppassword bahmni_reports > $BACKUP_PATH/bahmni_reports_$TIME.sql
pg_dump -U clinlims clinlims > $BACKUP_PATH/openelis_$TIME.sql
pg_dump -U odoo odoo > $BACKUP_PATH/odoo_$TIME.sql
bahmni -i local backup
service openmrs start
service bahmni-reports start
service bahmni-lab start
service odoo start
echo "Completed openmrs, bahmni-reports, openelis and odoo dbs backups"
echo "Deleting old files"
find $BACKUP_PATH/*.sql -mtime +90 -type f -delete
