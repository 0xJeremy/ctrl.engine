# Install the xbox driver

sudo apt-get install xboxdrv

# Adds the current user to the root group (to allow usage of xboxdrv)
# Comment out this line if you do not want the current user to be added.

sudo usermod -a -G root "$USER"

# Updates the permissions. Comment out this line if this is not desired behavior.

echo "KERNEL==\"uinput\", MODE=\"0660\", GROUP=\"root\"" > /etc/udev/rules.d/55-permissions-uinput.rules

echo "Done!"
