#! /bin/bash

git config --global --replace-all safe.directory /workspace

# Fix permissions for SSH agent socket
if [ -S /run/host-services/ssh-auth.sock ]; then
	sudo chmod 666 /run/host-services/ssh-auth.sock
	ssh_group="$(stat -c '%G' /run/host-services/ssh-auth.sock)"
	if [ -n "$ssh_group" ]; then
		sudo usermod -a -G "$ssh_group" vscode
	fi
fi

echo "=============== postStartCommand ran successfully. ==============="
