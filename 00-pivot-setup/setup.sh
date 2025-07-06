echo "-- Installing OCI-CLI"
sudo runuser -l opc -c 'mkdir -p /home/opc/oci_cli'
sudo runuser -l opc -c 'wget https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh'
sudo runuser -l opc -c 'chmod +x install.sh'
sudo runuser -l opc -c '/home/opc/install.sh --install-dir /home/opc/oci_cli/lib/oracle-cli --exec-dir /home/opc/oci_cli/bin --accept-all-defaults'
sudo runuser -l opc -c 'cp -rl /home/opc/bin /home/opc/oci_cli'
sudo runuser -l opc -c 'rm -r /home/opc/bin'
sudo runuser -l opc -c 'mkdir -p /home/opc/.oci'
sudo runuser -l opc -c 'touch /home/opc/.oci/config'
sudo runuser -l opc -c 'oci setup repair-file-permissions --file /home/opc/.oci/config'
echo -e "-- Done.\n\n"


echo "--  Installing Oracle Functions CLI"
curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh
echo "-- Done"

echo "-- Fixing Terminal watch for VSCode"
echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
echo "-- Done"