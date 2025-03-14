#!/bin/bash
if [ "$(whoami)" != "bahmni" ]; then
        echo "*** ATTENTION PLEASE!!! SCRIPT MUST BE RUN AS bahmni USER"
        exit -1
fi
echo "*** Starting cameroon implementation upgrade. NOTE: This upgrade will merge the html, omods and metadata repos into the config repo"
sudo -v
echo -n Please enter mysql root password: 
read -s mysql_password
echo

echo "*** Backing up logo and hospital name info"
cd ~
mkdir -p clinic-logo-and-name-backup
cd clinic-logo-and-name-backup
cp ../git/cameroon-bahmni-config/openmrs/apps/home/whiteLabel.json .
cp ../git/cameroon-bahmni-config/html/images/hospitalLogo.png .
# Added this in case we are upgrading from v1.3.0 to v1.13.0
cp ../git/cameroon-bahmni-html/html/images/hospitalLogo.png .
echo "*** Completed backing up logo and hospital name info"

echo "*** Deleting existing sources"
cd ~
rm -rf cameroon-bahmniapps
rm -rf dist-v1.13.0.zip
echo "*** Completed deleting existing sources"

echo "*** bahmniapps upgrade"
cd ~
wget -c https://github.com/jembi/cameroon-openmrs-module-bahmniapps/releases/download/v1.13.0/dist-v1.13.0.zip
mkdir -p cameroon-bahmniapps
unzip -q dist-v1.13.0.zip -d cameroon-bahmniapps
echo "*** Completed bahmniapps upgrade"

echo "*** bahmni-config upgrade"
rm -rf ~/git/cameroon-bahmni-config
cd ~/git
git clone https://github.com/jembi/cameroon-bahmni-config.git
cd cameroon-bahmni-config
git checkout v1.13.0
cp ~/clinic-logo-and-name-backup/whiteLabel.json ~/git/cameroon-bahmni-config/openmrs/apps/home/whiteLabel.json
cp ~/clinic-logo-and-name-backup/hospitalLogo.png ~/git/cameroon-bahmni-config/html/images/hospitalLogo.png
echo "*** Completed bahmni-config upgrade"

# Left this section in case the upgrade is from v1.3.0 to v1.13.0
echo "*** Remove old repos"
sudo rm -rf ~/git/cameroon-bahmni-metadata
sudo rm -rf ~/git/cameroon-bahmni-omods
sudo rm -rf ~/git/cameroon-bahmni-html
echo "*** Completed remove old repos"

echo "*** Links upgrade"
sudo rm -rf /opt/openmrs/configuration
sudo ln -s ~/git/cameroon-bahmni-config/metadata/configuration /opt/openmrs/configuration
sudo chown -h bahmni:bahmni /opt/openmrs/configuration

sudo rm -rf /var/www/html
sudo ln -s ~/git/cameroon-bahmni-config/html /var/www/html
sudo chown -h bahmni:bahmni /var/www/html

sudo rm -rf /opt/openmrs/modules
sudo ln -s ~/git/cameroon-bahmni-config/omods/modules /opt/openmrs/modules
sudo chown -h bahmni:bahmni /opt/openmrs/modules
echo "*** Completed links upgrade"
# end of section

echo "*** Restarting openmrs. This might take up to 20 minutes."
OPEMRSLOGDIR="/opt/openmrs/log"
OPEMRSBACKUPLOGDIR="/opt/openmrs/old_logs"
HOUR=`date +%d_%m_%Y_%H_%M_%S`
sudo mkdir -p $OPEMRSBACKUPLOGDIR/$HOUR
counter=0
sudo mv $OPEMRSLOGDIR/* $OPEMRSBACKUPLOGDIR/$HOUR
sudo service openmrs restart
while ! grep "InitializerActivator - Start of initializer module." /opt/openmrs/log/openmrs.log;
do
echo "Openmrs busy restarting..."
counter=$((counter+1))
echo "*** Time elapsed : " $counter
sleep 60
done
sleep 60
echo "*** Completed restarting openmrs"

echo "*** Openmrs sql scripts upgrade"
mysql -uroot -p$mysql_password openmrs < <(cat /home/bahmni/git/cameroon-bahmni-config/metadata/sql/*.sql)
mysql -uroot -p$mysql_password openmrs < <(cat /home/bahmni/git/cameroon-bahmni-config/metadata/reportssql/*.sql)
echo "Running script setProgramARVStartDate..."
wget -c https://github.com/jembi/cameroon-openmrs-module-bahmniapps/releases/download/v1.13.0/setProgramARVStartDate.sql
mysql -uroot -p$mysql_password openmrs < setProgramARVStartDate.sql
echo "*** Completed openmrs sql scripts upgrade"
