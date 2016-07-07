#!/bin/sh

export EXHIBITOR_USER=$RANDOM$RANDOM
export EXHIBITOR_PASSWORD=$RANDOM$RANDOM
envsubst < "$PKG_PATH"/stratiopaas-exhibitor-realm.properties.original > "$PKG_PATH"/stratiopaas-exhibitor-realm.properties
