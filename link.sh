#!/bin/bash

pkg-config --exists "libudjat"
if [ "${?}" != "0" ]; then
	echo "udjat-devel is required"
	exit -1
fi

if [ "${UID}" != "0" ]; then
	sudo $(readlink -f ${0}) ${@}
	exit ${?}
fi

PRODUCT_NAME=$(pkg-config --variable=product_name libudjat)

mkdir -p "/srv/www/htdocs/${PRODUCT_NAME}/icons"
if [ "${?}" != "0" ]; then
	echo "Unable to create /srv/www/htdocs/${PRODUCT_NAME}/icons"
	exit -1
fi

ln -sf $(readlink -f icons/*.svg) "/srv/www/htdocs/${PRODUCT_NAME}/icons"
if [ "${?}" != "0" ]; then
	echo "Unable to link icons to /srv/www/htdocs/${PRODUCT_NAME}/icons"
	exit -1
fi




