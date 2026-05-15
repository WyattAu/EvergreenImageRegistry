# Wolfi Package Audit Report

**Generated**: Automated audit against wolfi APKINDEX

**Source**: `https://packages.wolfi.dev/os/x86_64/APKINDEX.tar.gz`

## Summary

| Metric                     | Value |
| -------------------------- | ----- |
| Total unique packages      | 313   |
| Valid (in wolfi)           | 78    |
| Invalid (not in wolfi)     | 235   |
| Valid percentage           | 24.9% |
| Dockerfiles scanned        | 1014  |
| Dockerfiles with `apk add` | 394   |

## Invalid Packages

| Package                          | Category   | Dockerfiles | Images                                                                                                                     |
| -------------------------------- | ---------- | ----------- | -------------------------------------------------------------------------------------------------------------------------- |
| `apt-transport-https`            | unknown    | 6           | collabora-online, collabora-online-code, onlyoffice-communityserver, onlyoffice-controlpanel, onlyoffice-documentserver... |
| `chkrootkit`                     | unknown    | 1           | chkrootkit                                                                                                                 |
| `cockpit`                        | unknown    | 1           | cockpit                                                                                                                    |
| `cockpit-dashboard`              | unknown    | 1           | cockpit                                                                                                                    |
| `cockpit-storaged`               | unknown    | 1           | cockpit                                                                                                                    |
| `cockpit-system`                 | unknown    | 1           | cockpit                                                                                                                    |
| `cockpit-ws`                     | unknown    | 1           | cockpit                                                                                                                    |
| `conntrack`                      | unknown    | 1           | kube-proxy                                                                                                                 |
| `courier-authlib`                | unknown    | 2           | courier-authlib, courier-imap                                                                                              |
| `courier-imap`                   | unknown    | 1           | courier-imap                                                                                                               |
| `curl-openssl-dev`               | unknown    | 1           | modsecurity-crs                                                                                                            |
| `cyrus-sasl2-bin`                | unknown    | 1           | 389ds                                                                                                                      |
| `default-php84-mysql-client`     | unknown    | 4           | mysql-anonymizer, mysql-backup, mysql-init, mysql-restore                                                                  |
| `default-php84-mysql-server`     | unknown    | 2           | mariadb, mysql                                                                                                             |
| `dovecot-core`                   | unknown    | 3           | dovecot, dovecot-lda, dovecot-pop3                                                                                         |
| `dovecot-imapd`                  | unknown    | 2           | dovecot, dovecot-lda                                                                                                       |
| `dovecot-lmtpd`                  | unknown    | 2           | dovecot, dovecot-lda                                                                                                       |
| `dovecot-pop3d`                  | unknown    | 2           | dovecot, dovecot-pop3                                                                                                      |
| `erlang-asn1`                    | unknown    | 8           | couchdb, couchdb-sync, rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation...                                             |
| `erlang-base`                    | unknown    | 8           | couchdb, couchdb-sync, rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation...                                             |
| `erlang-crypto`                  | unknown    | 8           | couchdb, couchdb-sync, rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation...                                             |
| `erlang-eldap`                   | unknown    | 6           | rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation, rabbitmq-management, rabbitmq-mqtt...                                |
| `erlang-ftp`                     | unknown    | 6           | rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation, rabbitmq-management, rabbitmq-mqtt...                                |
| `erlang-inets`                   | unknown    | 6           | rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation, rabbitmq-management, rabbitmq-mqtt...                                |
| `erlang-mnesia`                  | unknown    | 6           | rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation, rabbitmq-management, rabbitmq-mqtt...                                |
| `erlang-os-mon`                  | unknown    | 6           | rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation, rabbitmq-management, rabbitmq-mqtt...                                |
| `erlang-parsetools`              | unknown    | 6           | rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation, rabbitmq-management, rabbitmq-mqtt...                                |
| `erlang-public-key`              | unknown    | 8           | couchdb, couchdb-sync, rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation...                                             |
| `erlang-runtime-tools`           | unknown    | 6           | rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation, rabbitmq-management, rabbitmq-mqtt...                                |
| `erlang-snmp`                    | unknown    | 6           | rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation, rabbitmq-management, rabbitmq-mqtt...                                |
| `erlang-ssl`                     | unknown    | 8           | couchdb, couchdb-sync, rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation...                                             |
| `erlang-syntax-tools`            | unknown    | 8           | couchdb, couchdb-sync, rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation...                                             |
| `erlang-tftp`                    | unknown    | 6           | rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation, rabbitmq-management, rabbitmq-mqtt...                                |
| `erlang-tools`                   | unknown    | 8           | couchdb, couchdb-sync, rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation...                                             |
| `erlang-xmerl`                   | unknown    | 6           | rabbitmq-amqp, rabbitmq-delayed, rabbitmq-federation, rabbitmq-management, rabbitmq-mqtt...                                |
| `fonts-liberation`               | unknown    | 1           | grafana-image-renderer                                                                                                     |
| `galera-4`                       | unknown    | 1           | mariadb-galera                                                                                                             |
| `golang`                         | unknown    | 1           | linguist-go                                                                                                                |
| `golang-go`                      | unknown    | 1           | golang                                                                                                                     |
| `imagick`                        | unknown    | 1           | nextcloud-imaging                                                                                                          |
| `imap`                           | unknown    | 1           | suitecrm                                                                                                                   |
| `java-17-runtime`                | unknown    | 55          | adempiere, airbyte, airbyte-server, airbyte-worker, airsonic...                                                            |
| `krb5-user`                      | unknown    | 1           | freeipa-client                                                                                                             |
| `ldap-utils`                     | unknown    | 3           | 389ds, openldap-backup, openldap-lambda                                                                                    |
| `libaio1`                        | debian-lib | 1           | oracledb-xe                                                                                                                |
| `libaio1t64`                     | debian-lib | 1           | mysql-8                                                                                                                    |
| `libapache-dbi-perl`             | unknown    | 1           | sql-ledger                                                                                                                 |
| `libapache2-mod-perl2`           | debian-lib | 1           | sql-ledger                                                                                                                 |
| `libapache2-mod-security2`       | debian-lib | 1           | modsecurity-crs                                                                                                            |
| `libasound2`                     | debian-lib | 1           | redis-insight                                                                                                              |
| `libasound2t64`                  | debian-lib | 1           | grafana-image-renderer                                                                                                     |
| `libass9`                        | debian-lib | 1           | jellyfin-ffmpeg                                                                                                            |
| `libatk-bridge2.0-0`             | unknown    | 1           | redis-insight                                                                                                              |
| `libatk-bridge2.0-0t64`          | unknown    | 1           | grafana-image-renderer                                                                                                     |
| `libatk1.0-0`                    | unknown    | 1           | redis-insight                                                                                                              |
| `libatspi2.0-0`                  | unknown    | 1           | redis-insight                                                                                                              |
| `libavahi-compat-libdnssd1`      | unknown    | 2           | homebridge, homebridge-camera                                                                                              |
| `libboost-all1.74`               | unknown    | 1           | memgraph                                                                                                                   |
| `libboost-all1.74-dev`           | unknown    | 1           | dnsdist                                                                                                                    |
| `libboost-filesystem1.74.0`      | unknown    | 2           | powerdns-api, powerdns-recursor                                                                                            |
| `libboost-iostreams1.74.0`       | unknown    | 1           | ledger                                                                                                                     |
| `libboost-program-options1.74.0` | unknown    | 2           | powerdns-api, powerdns-recursor                                                                                            |
| `libboost-system1.74.0`          | unknown    | 2           | powerdns-api, powerdns-recursor                                                                                            |
| `libboost-thread1.74.0`          | unknown    | 2           | powerdns-api, powerdns-recursor                                                                                            |
| `libcairo2`                      | debian-lib | 1           | redis-insight                                                                                                              |
| `libcgi-pm-perl`                 | unknown    | 1           | sql-ledger                                                                                                                 |
| `libcjson4`                      | debian-lib | 1           | nheko                                                                                                                      |
| `libcups2`                       | debian-lib | 1           | redis-insight                                                                                                              |
| `libdbd-pg-perl`                 | unknown    | 1           | sql-ledger                                                                                                                 |
| `libdbi-perl`                    | unknown    | 1           | sql-ledger                                                                                                                 |
| `libdbus-1-3`                    | unknown    | 1           | redis-insight                                                                                                              |
| `libdrm2`                        | debian-lib | 1           | redis-insight                                                                                                              |
| `libedit2`                       | debian-lib | 1           | cubrid                                                                                                                     |
| `libelf1`                        | debian-lib | 1           | vpn-controller                                                                                                             |
| `libevent-2.1-7`                 | versioned  | 1           | couchbase                                                                                                                  |
| `libfdk-acct2`                   | unknown    | 1           | jellyfin-ffmpeg                                                                                                            |
| `libgbm1`                        | debian-lib | 2           | grafana-image-renderer, redis-insight                                                                                      |
| `libgcc-s1`                      | unknown    | 2           | zeromq, zerotier                                                                                                           |
| `libgeoip-dev`                   | unknown    | 1           | modsecurity-crs                                                                                                            |
| `libgeoip1`                      | debian-lib | 1           | nginx-modsec                                                                                                               |
| `libgl1`                         | debian-lib | 1           | nheko                                                                                                                      |
| `libgmp10`                       | debian-lib | 3           | ledger, ocserv, strongswan                                                                                                 |
| `libgnutls30`                    | debian-lib | 1           | ocserv                                                                                                                     |
| `libgomp1`                       | debian-lib | 1           | splunk-forwarder                                                                                                           |
| `libgrpc++1`                     | unknown    | 1           | memgraph                                                                                                                   |
| `libgtk-3-0`                     | unknown    | 2           | cyberduck, ldapbrowser                                                                                                     |
| `libgtk-3-0t64`                  | unknown    | 1           | grafana-image-renderer                                                                                                     |
| `libhogweed6`                    | debian-lib | 1           | ocserv                                                                                                                     |
| `libice6`                        | debian-lib | 2           | emby, emby-server                                                                                                          |
| `libicu72`                       | debian-lib | 4           | couchdb, couchdb-sync, mattermost, postgresql-17                                                                           |
| `libidn2-0`                      | debian-lib | 1           | dnsmasq-full                                                                                                               |
| `libjpeg-turbo-turbo-dev`        | unknown    | 5           | authentik, authentik-worker, sentry, sentry-cron, sentry-worker                                                            |
| `libjson-c5`                     | unknown    | 1           | falco                                                                                                                      |
| `libjson-perl`                   | unknown    | 1           | sql-ledger                                                                                                                 |
| `liblua5.3-0`                    | unknown    | 1           | dnsdist                                                                                                                    |
| `libluajit-5.1-2`                | versioned  | 2           | knot-resolver, powerdns-recursor                                                                                           |
| `liblzma5`                       | debian-lib | 1           | nxlog                                                                                                                      |
| `liblzo2-2`                      | debian-lib | 1           | openvpn-as                                                                                                                 |
| `libmariadb3`                    | debian-lib | 3           | openproject, redmine, vaultwarden-mysql                                                                                    |
| `libmecab2`                      | debian-lib | 1           | mysql-8                                                                                                                    |
| `libmilter1.0.1`                 | unknown    | 1           | rmilter                                                                                                                    |
| `libmnl0`                        | debian-lib | 1           | vpn-controller                                                                                                             |
| `libmodsecurity3`                | debian-lib | 1           | modsecurity-crs                                                                                                            |
| `libmozjs-78-0`                  | unknown    | 2           | couchdb, couchdb-sync                                                                                                      |
| `libmp3lame0`                    | debian-lib | 1           | jellyfin-ffmpeg                                                                                                            |
| `libmpfr6`                       | debian-lib | 1           | ledger                                                                                                                     |
| `libncurses5`                    | debian-lib | 1           | cubrid                                                                                                                     |
| `libncurses6`                    | debian-lib | 1           | tig                                                                                                                        |
| `libnetfilter-conntrack3`        | unknown    | 1           | dnsmasq-full                                                                                                               |
| `libnettle8`                     | debian-lib | 1           | ocserv                                                                                                                     |
| `libnspr4`                       | debian-lib | 1           | redis-insight                                                                                                              |
| `libnss3`                        | debian-lib | 4           | grafana-image-renderer, kibana, kibana-oss, redis-insight                                                                  |
| `libnss3-tools`                  | debian-lib | 1           | freeipa-client                                                                                                             |
| `libnuma1`                       | debian-lib | 1           | mysql-8                                                                                                                    |
| `libodbc1`                       | debian-lib | 2           | emqx, emqx-ee                                                                                                              |
| `libopenscap8`                   | debian-lib | 1           | openscap                                                                                                                   |
| `libopus0`                       | debian-lib | 1           | jellyfin-ffmpeg                                                                                                            |
| `libpam-sss`                     | unknown    | 1           | freeipa-client                                                                                                             |
| `libpam0g`                       | unknown    | 1           | ocserv                                                                                                                     |
| `libpango-1.0-0`                 | versioned  | 1           | redis-insight                                                                                                              |
| `libpcre3`                       | debian-lib | 3           | nginx-alpine, nginx-cache, nginx-modsec                                                                                    |
| `libpcre3-dev`                   | debian-lib | 1           | modsecurity-crs                                                                                                            |
| `libpkcs11-helper1`              | debian-lib | 1           | openvpn-as                                                                                                                 |
| `libprotobuf32`                  | debian-lib | 3           | dnsdist, memgraph, rethinkdb                                                                                               |
| `libpython3.11`                  | unknown    | 2           | dnsvalidator, surrealdb-python                                                                                             |
| `libqscintilla2-qt5-15`          | debian-lib | 1           | sqlite-browser                                                                                                             |
| `libqt5core5a`                   | unknown    | 1           | eqonomize                                                                                                                  |
| `libqt5core5t64`                 | debian-lib | 1           | sqlite-browser                                                                                                             |
| `libqt5gui5`                     | debian-lib | 1           | eqonomize                                                                                                                  |
| `libqt5gui5t64`                  | debian-lib | 1           | sqlite-browser                                                                                                             |
| `libqt5network5t64`              | debian-lib | 1           | sqlite-browser                                                                                                             |
| `libqt5svg5`                     | debian-lib | 1           | sqlite-browser                                                                                                             |
| `libqt5widgets5`                 | debian-lib | 1           | eqonomize                                                                                                                  |
| `libqt5widgets5t64`              | debian-lib | 1           | sqlite-browser                                                                                                             |
| `libqt6core6`                    | debian-lib | 1           | nheko                                                                                                                      |
| `libqt6gui6`                     | debian-lib | 1           | nheko                                                                                                                      |
| `libqt6multimedia6`              | debian-lib | 1           | nheko                                                                                                                      |
| `libqt6network6`                 | debian-lib | 1           | nheko                                                                                                                      |
| `libqt6qml6`                     | debian-lib | 1           | nheko                                                                                                                      |
| `libqt6quick6`                   | debian-lib | 1           | nheko                                                                                                                      |
| `libqt6widgets6`                 | debian-lib | 1           | nheko                                                                                                                      |
| `libre2-5`                       | debian-lib | 1           | dnsdist                                                                                                                    |
| `libreadline8`                   | debian-lib | 1           | postgresql-17                                                                                                              |
| `libsasl2-modules`               | debian-lib | 2           | 389ds, openldap-lambda                                                                                                     |
| `libseccomp2`                    | debian-lib | 1           | ocserv                                                                                                                     |
| `libsm6`                         | debian-lib | 2           | emby, emby-server                                                                                                          |
| `libsnappy1v5`                   | debian-lib | 1           | couchbase                                                                                                                  |
| `libsodium23`                    | debian-lib | 2           | dnsdist, zeromq                                                                                                            |
| `libsqlcipher0`                  | debian-lib | 1           | sqlite-browser                                                                                                             |
| `libswt-gtk-4-java`              | unknown    | 2           | cyberduck, ldapbrowser                                                                                                     |
| `libtasn1-6`                     | debian-lib | 1           | ocserv                                                                                                                     |
| `libtemplate-perl`               | unknown    | 1           | sql-ledger                                                                                                                 |
| `libtheora0`                     | debian-lib | 1           | jellyfin-ffmpeg                                                                                                            |
| `libusb-1.0-0`                   | versioned  | 1           | openhab3                                                                                                                   |
| `libuv1`                         | debian-lib | 1           | knot-resolver                                                                                                              |
| `libvorbis0a`                    | unknown    | 1           | jellyfin-ffmpeg                                                                                                            |
| `libvpx7`                        | debian-lib | 1           | jellyfin-ffmpeg                                                                                                            |
| `libwebp7`                       | debian-lib | 1           | jellyfin-ffmpeg                                                                                                            |
| `libwrap0`                       | debian-lib | 2           | ocserv, pptpd                                                                                                              |
| `libx11-6`                       | debian-lib | 5           | emby, emby-server, plex, plex-media-server, redis-insight                                                                  |
| `libx264-164`                    | debian-lib | 1           | jellyfin-ffmpeg                                                                                                            |
| `libx265-199`                    | debian-lib | 1           | jellyfin-ffmpeg                                                                                                            |
| `libxcb1`                        | debian-lib | 2           | plex, plex-media-server                                                                                                    |
| `libxcomposite1`                 | debian-lib | 1           | redis-insight                                                                                                              |
| `libxdamage1`                    | debian-lib | 3           | plex, plex-media-server, redis-insight                                                                                     |
| `libxext6`                       | debian-lib | 5           | emby, emby-server, plex, plex-media-server, redis-insight                                                                  |
| `libxfixes3`                     | debian-lib | 3           | plex, plex-media-server, redis-insight                                                                                     |
| `libxi6`                         | debian-lib | 1           | redis-insight                                                                                                              |
| `libxkbcommon0`                  | debian-lib | 1           | redis-insight                                                                                                              |
| `libxrandr2`                     | debian-lib | 1           | redis-insight                                                                                                              |
| `libxrender1`                    | debian-lib | 5           | emby, emby-server, plex, plex-media-server, redis-insight                                                                  |
| `libxss1`                        | debian-lib | 3           | grafana-image-renderer, plex, plex-media-server                                                                            |
| `libxtst6`                       | debian-lib | 3           | plex, plex-media-server, redis-insight                                                                                     |
| `libxvidcore4`                   | debian-lib | 1           | jellyfin-ffmpeg                                                                                                            |
| `libyajl-dev`                    | unknown    | 1           | modsecurity-crs                                                                                                            |
| `libyajl2`                       | debian-lib | 1           | nginx-modsec                                                                                                               |
| `libyaml-0-2`                    | unknown    | 1           | falco                                                                                                                      |
| `libyaml-cpp0.7`                 | unknown    | 1           | dnsdist                                                                                                                    |
| `libyaml-dev`                    | unknown    | 3           | sentry, sentry-cron, sentry-worker                                                                                         |
| `libz1`                          | debian-lib | 3           | nginx-alpine, nginx-cache, nginx-modsec                                                                                    |
| `lsb-release`                    | unknown    | 2           | mysql-8, postgresql-17                                                                                                     |
| `mailutils`                      | unknown    | 1           | postfix                                                                                                                    |
| `mariadb-server`                 | unknown    | 3           | mariadb-10, mariadb-11, mariadb-galera                                                                                     |
| `mongodb-org`                    | unknown    | 2           | mongodb, mongodb-6                                                                                                         |
| `mongodb-org-tools`              | unknown    | 1           | realm-server                                                                                                               |
| `musl-dev`                       | unknown    | 2           | musl, x86_64-unknown-linux-musl                                                                                            |
| `nginx-light`                    | unknown    | 4           | cinny, element-web, element-x, hydrogen                                                                                    |
| `oddjob-mkhomedir`               | unknown    | 1           | freeipa-client                                                                                                             |
| `openjdk-21-jre-headless`        | unknown    | 3           | keycloak, keycloak-init, keycloak-quarkus                                                                                  |
| `openjdk-__VAR__-jre-headless`   | unknown    | 2           | activemq, rocketmq                                                                                                         |
| `openscap-utils`                 | unknown    | 1           | openscap                                                                                                                   |
| `openssl-libs`                   | unknown    | 28          | arango, couchbase, dnsdist, emqx, emqx-ee...                                                                               |
| `php84`                          | unknown    | 19          | akaunting, composer-audit, dolibarr, egroupware, espocrm...                                                                |
| `php84-bcmath`                   | unknown    | 1           | cachet                                                                                                                     |
| `php84-curl`                     | unknown    | 21          | akaunting, cachet, composer-audit, dolibarr, egroupware...                                                                 |
| `php84-fpm`                      | unknown    | 21          | akaunting, cachet, dolibarr, egroupware, espocrm...                                                                        |
| `php84-gd`                       | unknown    | 13          | dolibarr, egroupware, espocrm, invoice-ninja, invoice-ninja-api...                                                         |
| `php84-intl`                     | unknown    | 15          | akaunting, dolibarr, egroupware, espocrm, frontaccounting...                                                               |
| `php84-mbstring`                 | unknown    | 15          | akaunting, dolibarr, egroupware, espocrm, frontaccounting...                                                               |
| `php84-mysql`                    | unknown    | 15          | akaunting, dolibarr, egroupware, espocrm, frontaccounting...                                                               |
| `php84-pdo`                      | unknown    | 9           | akaunting, dolibarr, egroupware, espocrm, frontaccounting...                                                               |
| `php84-pgsql`                    | unknown    | 1           | cachet                                                                                                                     |
| `php84-php84-gd`                 | unknown    | 2           | cachet, privatebin-nginx                                                                                                   |
| `php84-php84-intl`               | unknown    | 2           | rainloop, roundcube                                                                                                        |
| `php84-php84-mbstring`           | unknown    | 6           | cachet, composer-audit, ldap-account-manager, privatebin-nginx, rainloop...                                                |
| `php84-php84-mysql`              | unknown    | 1           | cachet                                                                                                                     |
| `php84-php84-xml`                | unknown    | 6           | cachet, composer-audit, ldap-account-manager, privatebin-nginx, rainloop...                                                |
| `php84-redis`                    | unknown    | 1           | cachet                                                                                                                     |
| `php84-sqlite-libs`              | unknown    | 2           | cachet, organizer                                                                                                          |
| `php84-xml`                      | unknown    | 15          | akaunting, dolibarr, egroupware, espocrm, frontaccounting...                                                               |
| `php84-zip`                      | unknown    | 3           | cachet, rainloop, roundcube                                                                                                |
| `postgresql-16-postgis-3`        | unknown    | 1           | postgis                                                                                                                    |
| `postgresql-16-timescaledb`      | unknown    | 1           | timescaledb                                                                                                                |
| `postgresql-client-17`           | unknown    | 1           | postgresql-anonymizer                                                                                                      |
| `postgresql-client-__VAR__`      | unknown    | 3           | postgres-backup, postgres-restore, postgresql-init                                                                         |
| `postgresql-libs`                | unknown    | 15          | authentik, authentik-geoip, authentik-proxy, authentik-worker, erpnext-worker...                                           |
| `postgrey`                       | unknown    | 1           | postgrey                                                                                                                   |
| `ppp`                            | unknown    | 1           | pptpd                                                                                                                      |
| `python3-minimal`                | unknown    | 4           | awslogs, azurelogs, gcplogs, python                                                                                        |
| `redis`                          | unknown    | 3           | redis, redis-6, redis-7                                                                                                    |
| `rkhunter`                       | unknown    | 1           | rkhunter                                                                                                                   |
| `ruby3.1`                        | unknown    | 2           | openproject, redmine                                                                                                       |
| `scap-workbench`                 | unknown    | 1           | scap-workbench                                                                                                             |
| `slapd`                          | unknown    | 2           | 389ds, openldap-backup                                                                                                     |
| `soap`                           | unknown    | 2           | dolibarr, vtigercrm                                                                                                        |
| `spamassassin`                   | unknown    | 1           | spamassassin                                                                                                               |
| `spamc`                          | unknown    | 1           | spamassassin                                                                                                               |
| `sssd`                           | unknown    | 1           | freeipa-client                                                                                                             |
| `sssd-tools`                     | unknown    | 1           | freeipa-client                                                                                                             |
| `syslog-ng-core`                 | unknown    | 1           | syslog-ng                                                                                                                  |
| `temurin-21-jre-headless`        | unknown    | 1           | openjdk-alpine                                                                                                             |
| `virtuoso-opensource`            | unknown    | 1           | virtuoso                                                                                                                   |
| `virtuoso-opensource-7`          | unknown    | 1           | virtuoso                                                                                                                   |
| `xz-utils`                       | unknown    | 4           | mysql-backup, mysql-restore, postgres-backup, postgres-restore                                                             |
| `zlib1g-dev`                     | unknown    | 5           | authentik, authentik-worker, sentry, sentry-cron, sentry-worker                                                            |

## Category Breakdown

| Category   | Count | Examples                                                                                  |
| ---------- | ----- | ----------------------------------------------------------------------------------------- |
| debian-lib | 91    | `libaio1`, `libaio1t64`, `libapache2-mod-perl2`, `libapache2-mod-security2`, `libasound2` |
| debian-php | 0     | —                                                                                         |
| versioned  | 4     | `libevent-2.1-7`, `libluajit-5.1-2`, `libpango-1.0-0`, `libusb-1.0-0`                     |
| unknown    | 140   | `apt-transport-https`, `chkrootkit`, `cockpit`, `cockpit-dashboard`, `cockpit-storaged`   |

## Per-Image Summary

### `389ds`

**Valid** (2): `ca-certificates`, `openldap`

**Invalid** (4): `cyrus-sasl2-bin`, `ldap-utils`, `libsasl2-modules`, `slapd`

### `activemq`

**Valid** (1): `ca-certificates`

**Invalid** (1): `openjdk-__VAR__-jre-headless`

### `adempiere`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `airbyte`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `airbyte-server`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `airbyte-worker`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `airsonic`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `airsonic-advanced`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `akaunting`

**Valid** (4): `ca-certificates`, `nginx`, `openssl`, `zip`

**Invalid** (8): `php84`, `php84-curl`, `php84-fpm`, `php84-intl`, `php84-mbstring`, `php84-mysql`, `php84-pdo`,
`php84-xml`

### `alpine`

**Valid** (2): `ca-certificates`, `tzdata`

All packages valid.

### `apache-nifi`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `apache-ofbiz`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `appsmith`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `appsmith-editor`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `appsmith-nginx`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `arango`

**Valid** (2): `ca-certificates`, `libstdc++`

**Invalid** (1): `openssl-libs`

### `argocd-redis`

**Valid** (1): `ca-certificates`

All packages valid.

### `arm64`

**Valid** (2): `ca-certificates`, `tzdata`

All packages valid.

### `audiobookshelf`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `audiobookshelf-opds`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `authentik`

**Valid** (8): `build-base`, `ca-certificates`, `libffi-dev`, `libxml2-dev`, `libxslt-dev`, `openssl-dev`, `py3-pip`,
`python3`

**Invalid** (3): `libjpeg-turbo-turbo-dev`, `postgresql-libs`, `zlib1g-dev`

### `authentik-geoip`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

**Invalid** (1): `postgresql-libs`

### `authentik-proxy`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

**Invalid** (1): `postgresql-libs`

### `authentik-worker`

**Valid** (8): `build-base`, `ca-certificates`, `libffi-dev`, `libxml2-dev`, `libxslt-dev`, `openssl-dev`, `py3-pip`,
`python3`

**Invalid** (3): `libjpeg-turbo-turbo-dev`, `postgresql-libs`, `zlib1g-dev`

### `awslogs`

**Valid** (1): `ca-certificates`

**Invalid** (1): `python3-minimal`

### `azurelogs`

**Valid** (1): `ca-certificates`

**Invalid** (1): `python3-minimal`

### `basic-auth-proxy`

**Valid** (4): `apache2`, `ca-certificates`, `libpcre2-8-0`, `zlib`

All packages valid.

### `beancount`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `browserless`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `browserless-chrome`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `browserless-edge`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `budibase`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `budibase-worker`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `buildah`

**Valid** (2): `ca-certificates`, `containers-common`

All packages valid.

### `cachet`

**Valid** (2): `ca-certificates`, `nginx`

**Invalid** (11): `php84-bcmath`, `php84-curl`, `php84-fpm`, `php84-pgsql`, `php84-php84-gd`, `php84-php84-mbstring`,
`php84-php84-mysql`, `php84-php84-xml`, `php84-redis`, `php84-sqlite-libs`, `php84-zip`

### `caddy-alpine`

**Valid** (2): `ca-certificates`, `libcap`

All packages valid.

### `cargo-audit`

**Valid** (1): `ca-certificates`

All packages valid.

### `cassandra`

**Invalid** (1): `java-17-runtime`

### `chartdb`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `checkov`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `checkov-k8s`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `chkrootkit`

**Valid** (1): `ca-certificates`

**Invalid** (1): `chkrootkit`

### `cinny`

**Valid** (1): `ca-certificates`

**Invalid** (1): `nginx-light`

### `clamav`

**Valid** (3): `ca-certificates`, `clamav`, `clamav-daemon`

All packages valid.

### `clamav-daemon`

**Valid** (4): `ca-certificates`, `clamav`, `clamav-daemon`, `freshclam`

All packages valid.

### `cockpit`

**Valid** (1): `ca-certificates`

**Invalid** (5): `cockpit`, `cockpit-dashboard`, `cockpit-storaged`, `cockpit-system`, `cockpit-ws`

### `codimd`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `collabora-online`

**Valid** (2): `ca-certificates`, `gnupg`

**Invalid** (1): `apt-transport-https`

### `collabora-online-code`

**Valid** (2): `ca-certificates`, `gnupg`

**Invalid** (1): `apt-transport-https`

### `composer-audit`

**Valid** (2): `ca-certificates`, `unzip`

**Invalid** (4): `php84`, `php84-curl`, `php84-php84-mbstring`, `php84-php84-xml`

### `conan-audit`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `cors-proxy`

**Valid** (3): `ca-certificates`, `libpcre2-8-0`, `zlib`

All packages valid.

### `couchbase`

**Valid** (3): `libstdc++`, `procps`, `zlib`

**Invalid** (3): `libevent-2.1-7`, `libsnappy1v5`, `openssl-libs`

### `couchdb`

**Valid** (1): `procps`

**Invalid** (9): `erlang-asn1`, `erlang-base`, `erlang-crypto`, `erlang-public-key`, `erlang-ssl`,
`erlang-syntax-tools`, `erlang-tools`, `libicu72`, `libmozjs-78-0`

### `couchdb-sync`

**Valid** (1): `procps`

**Invalid** (9): `erlang-asn1`, `erlang-base`, `erlang-crypto`, `erlang-public-key`, `erlang-ssl`,
`erlang-syntax-tools`, `erlang-tools`, `libicu72`, `libmozjs-78-0`

### `courier-authlib`

**Invalid** (1): `courier-authlib`

### `courier-imap`

**Invalid** (2): `courier-authlib`, `courier-imap`

### `crate`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (1): `java-17-runtime`

### `cryptpad`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `cubrid`

**Valid** (1): `ca-certificates`

**Invalid** (2): `libedit2`, `libncurses5`

### `cyberchef`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `cyberchef-node`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `cyberduck`

**Valid** (1): `ca-certificates`

**Invalid** (3): `java-17-runtime`, `libgtk-3-0`, `libswt-gtk-4-java`

### `dashy-alpine`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `dependabot`

**Valid** (3): `ca-certificates`, `gnupg`, `ruby`

All packages valid.

### `derby`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `detect-secrets`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `dnsdist`

**Valid** (1): `ca-certificates`

**Invalid** (7): `libboost-all1.74-dev`, `liblua5.3-0`, `libprotobuf32`, `libre2-5`, `libsodium23`, `libyaml-cpp0.7`,
`openssl-libs`

### `dnsmasq-full`

**Valid** (1): `ca-certificates`

**Invalid** (2): `libidn2-0`, `libnetfilter-conntrack3`

### `dnsvalidator`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (1): `libpython3.11`

### `docker-bench`

**Valid** (1): `ca-certificates`

All packages valid.

### `docker-clean`

**Valid** (1): `ca-certificates`

All packages valid.

### `docker-gc`

**Valid** (1): `ca-certificates`

All packages valid.

### `dockerfile-lint`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `dolibarr`

**Valid** (5): `ca-certificates`, `json-c`, `nginx`, `openssl`, `zip`

**Invalid** (10): `php84`, `php84-curl`, `php84-fpm`, `php84-gd`, `php84-intl`, `php84-mbstring`, `php84-mysql`,
`php84-pdo`, `php84-xml`, `soap`

### `dovecot`

**Invalid** (4): `dovecot-core`, `dovecot-imapd`, `dovecot-lmtpd`, `dovecot-pop3d`

### `dovecot-lda`

**Valid** (1): `ca-certificates`

**Invalid** (3): `dovecot-core`, `dovecot-imapd`, `dovecot-lmtpd`

### `dovecot-pop3`

**Valid** (1): `ca-certificates`

**Invalid** (2): `dovecot-core`, `dovecot-pop3d`

### `druid`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (1): `java-17-runtime`

### `duplicati`

**Valid** (1): `ca-certificates`

All packages valid.

### `egroupware`

**Valid** (5): `ca-certificates`, `json-c`, `nginx`, `openssl`, `zip`

**Invalid** (9): `php84`, `php84-curl`, `php84-fpm`, `php84-gd`, `php84-intl`, `php84-mbstring`, `php84-mysql`,
`php84-pdo`, `php84-xml`

### `ejdb`

**Valid** (2): `ca-certificates`, `libstdc++`

All packages valid.

### `elasticsearch-8`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `elasticsearch-curator`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

All packages valid.

### `element-web`

**Valid** (1): `ca-certificates`

**Invalid** (1): `nginx-light`

### `element-x`

**Valid** (1): `ca-certificates`

**Invalid** (1): `nginx-light`

### `emby`

**Valid** (4): `ca-certificates`, `fontconfig`, `freetype`, `glib`

**Invalid** (5): `libice6`, `libsm6`, `libx11-6`, `libxext6`, `libxrender1`

### `emby-server`

**Valid** (4): `ca-certificates`, `fontconfig`, `freetype`, `glib`

**Invalid** (5): `libice6`, `libsm6`, `libx11-6`, `libxext6`, `libxrender1`

### `emqx`

**Valid** (2): `ca-certificates`, `procps`

**Invalid** (2): `libodbc1`, `openssl-libs`

### `emqx-ee`

**Valid** (2): `ca-certificates`, `procps`

**Invalid** (2): `libodbc1`, `openssl-libs`

### `eqonomize`

**Valid** (1): `ca-certificates`

**Invalid** (3): `libqt5core5a`, `libqt5gui5`, `libqt5widgets5`

### `erpnext-worker`

**Valid** (5): `ca-certificates`, `libjpeg-turbo`, `python3`, `tzdata`, `zlib`

**Invalid** (1): `postgresql-libs`

### `espeasy`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `esphome`

**Valid** (3): `ca-certificates`, `python3`, `tzdata`

All packages valid.

### `esphome-daemon`

**Valid** (3): `ca-certificates`, `python3`, `tzdata`

All packages valid.

### `espocrm`

**Valid** (5): `ca-certificates`, `json-c`, `nginx`, `openssl`, `zip`

**Invalid** (9): `php84`, `php84-curl`, `php84-fpm`, `php84-gd`, `php84-intl`, `php84-mbstring`, `php84-mysql`,
`php84-pdo`, `php84-xml`

### `espurna`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `falco`

**Valid** (1): `ca-certificates`

**Invalid** (2): `libjson-c5`, `libyaml-0-2`

### `falco-rules`

**Valid** (1): `ca-certificates`

All packages valid.

### `firefly-iii-importer`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `fluentd`

**Valid** (2): `ca-certificates`, `libffi-dev`

All packages valid.

### `focalboard-server`

**Valid** (1): `ca-certificates`

All packages valid.

### `forgejo`

**Valid** (1): `ca-certificates`

All packages valid.

### `freeipa-client`

**Valid** (1): `ca-certificates`

**Invalid** (6): `krb5-user`, `libnss3-tools`, `libpam-sss`, `oddjob-mkhomedir`, `sssd`, `sssd-tools`

### `freshclam`

**Valid** (2): `ca-certificates`, `clamav-freshclam`

All packages valid.

### `frontaccounting`

**Valid** (4): `ca-certificates`, `nginx`, `openssl`, `zip`

**Invalid** (8): `php84`, `php84-curl`, `php84-fpm`, `php84-intl`, `php84-mbstring`, `php84-mysql`, `php84-pdo`,
`php84-xml`

### `gcplogs`

**Valid** (1): `ca-certificates`

**Invalid** (1): `python3-minimal`

### `gem-audit`

**Valid** (2): `ca-certificates`, `ruby`

All packages valid.

### `ggshield`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `git-secrets`

**Valid** (1): `ca-certificates`

All packages valid.

### `gitbucket`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `gitea`

**Valid** (1): `ca-certificates`

All packages valid.

### `gitguardian`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `github-actions-minimal`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `gitlab-backup`

**Valid** (3): `ca-certificates`, `openssh-client`, `ruby`

All packages valid.

### `gitlab-ce`

**Valid** (4): `ca-certificates`, `gnupg`, `openssh-client`, `postfix`

All packages valid.

### `gitlab-ee`

**Valid** (4): `ca-certificates`, `gnupg`, `openssh-client`, `postfix`

All packages valid.

### `gitlab-geo`

**Valid** (4): `ca-certificates`, `gnupg`, `openssh-client`, `postgresql-client`

All packages valid.

### `golang`

**Valid** (1): `ca-certificates`

**Invalid** (1): `golang-go`

### `gradle`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `grafana`

**Valid** (3): `ca-certificates`, `fontconfig`, `tzdata`

All packages valid.

### `grafana-image-renderer`

**Valid** (1): `ca-certificates`

**Invalid** (7): `fonts-liberation`, `libasound2t64`, `libatk-bridge2.0-0t64`, `libgbm1`, `libgtk-3-0t64`, `libnss3`,
`libxss1`

### `graphdb-enterpriser`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `graphdb-free`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `graylog`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `h2`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `hackmd`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `haproxy`

**Valid** (1): `haproxy`

All packages valid.

### `haproxy-dev`

**Valid** (1): `haproxy`

All packages valid.

### `haproxy-lb`

**Valid** (1): `haproxy`

All packages valid.

### `hashicorp-vault-enterprise`

**Valid** (2): `ca-certificates`, `unzip`

All packages valid.

### `hazelcast`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `hedgedoc`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `hedgedoc-legacy`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `heimdall`

**Valid** (3): `ca-certificates`, `nginx`, `nodejs`

All packages valid.

### `heimdall-lite`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `hive`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `hive-metastore`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `homeassistant-core`

**Valid** (5): `ca-certificates`, `libffi-dev`, `openssl-dev`, `python3`, `tzdata`

All packages valid.

### `homeassistant-hassio`

**Valid** (6): `ca-certificates`, `dbus`, `libffi-dev`, `openssl-dev`, `python3`, `tzdata`

All packages valid.

### `homeassistant-supervisor`

**Valid** (5): `ca-certificates`, `dbus`, `jq`, `python3`, `tzdata`

All packages valid.

### `homebridge`

**Valid** (2): `ca-certificates`, `nodejs`

**Invalid** (1): `libavahi-compat-libdnssd1`

### `homebridge-camera`

**Valid** (3): `ca-certificates`, `ffmpeg`, `nodejs`

**Invalid** (1): `libavahi-compat-libdnssd1`

### `hydrogen`

**Valid** (1): `ca-certificates`

**Invalid** (1): `nginx-light`

### `idempiere`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `ignite`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `immich-microservices`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `immich-server`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `invoice-ninja`

**Valid** (4): `ca-certificates`, `nginx`, `openssl`, `zip`

**Invalid** (9): `php84`, `php84-curl`, `php84-fpm`, `php84-gd`, `php84-intl`, `php84-mbstring`, `php84-mysql`,
`php84-pdo`, `php84-xml`

### `invoice-ninja-api`

**Valid** (4): `ca-certificates`, `nginx`, `openssl`, `zip`

**Invalid** (9): `php84`, `php84-curl`, `php84-fpm`, `php84-gd`, `php84-intl`, `php84-mbstring`, `php84-mysql`,
`php84-pdo`, `php84-xml`

### `iobroker`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `it-tools-legacy`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `janusgraph`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `jellyfin-ffmpeg`

**Valid** (3): `ca-certificates`, `freetype`, `zlib`

**Invalid** (11): `libass9`, `libfdk-acct2`, `libmp3lame0`, `libopus0`, `libtheora0`, `libvorbis0a`, `libvpx7`,
`libwebp7`, `libx264-164`, `libx265-199`, `libxvidcore4`

### `jenkins-agent`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `jenkins-executor`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `jenkins-plugin`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `jitsu`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `kafka`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `kafka-connect`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `kafka-manager`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `kaniko`

**Valid** (1): `ca-certificates`

All packages valid.

### `keycloak`

**Valid** (1): `ca-certificates`

**Invalid** (1): `openjdk-21-jre-headless`

### `keycloak-init`

**Valid** (1): `ca-certificates`

**Invalid** (1): `openjdk-21-jre-headless`

### `keycloak-quarkus`

**Valid** (1): `ca-certificates`

**Invalid** (1): `openjdk-21-jre-headless`

### `kibana`

**Valid** (1): `ca-certificates`

**Invalid** (1): `libnss3`

### `kibana-oss`

**Valid** (1): `ca-certificates`

**Invalid** (1): `libnss3`

### `knot-resolver`

**Valid** (2): `ca-certificates`, `libnghttp2-14`

**Invalid** (3): `libluajit-5.1-2`, `libuv1`, `openssl-libs`

### `kube-apiserver`

**Valid** (1): `ca-certificates`

All packages valid.

### `kube-controller`

**Valid** (1): `ca-certificates`

All packages valid.

### `kube-hunter`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `kube-proxy`

**Valid** (2): `ca-certificates`, `iptables`

**Invalid** (1): `conntrack`

### `kube-scheduler`

**Valid** (1): `ca-certificates`

All packages valid.

### `ldap-account-manager`

**Valid** (2): `ca-certificates`, `php-ldap`

**Invalid** (4): `php84-curl`, `php84-fpm`, `php84-php84-mbstring`, `php84-php84-xml`

### `ldapbrowser`

**Valid** (1): `ca-certificates`

**Invalid** (3): `java-17-runtime`, `libgtk-3-0`, `libswt-gtk-4-java`

### `ledger`

**Valid** (1): `ca-certificates`

**Invalid** (3): `libboost-iostreams1.74.0`, `libgmp10`, `libmpfr6`

### `linguist`

**Valid** (2): `ca-certificates`, `ruby`

All packages valid.

### `linguist-go`

**Valid** (1): `ca-certificates`

**Invalid** (1): `golang`

### `logstash`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `logstash-oss`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `lynis`

**Valid** (1): `ca-certificates`

All packages valid.

### `mailtrain`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `mailu`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `maldet`

**Valid** (3): `ca-certificates`, `clamav-daemon`, `inotify-tools`

All packages valid.

### `mariadb`

**Valid** (1): `ca-certificates`

**Invalid** (1): `default-php84-mysql-server`

### `mariadb-10`

**Valid** (1): `ca-certificates`

**Invalid** (1): `mariadb-server`

### `mariadb-11`

**Valid** (1): `ca-certificates`

**Invalid** (1): `mariadb-server`

### `mariadb-galera`

**Valid** (4): `ca-certificates`, `mariadb-backup`, `rsync`, `socat`

**Invalid** (2): `galera-4`, `mariadb-server`

### `mattermost`

**Valid** (2): `ca-certificates`, `tzdata`

**Invalid** (1): `libicu72`

### `maven`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `memcached`

**Valid** (2): `ca-certificates`, `memcached`

All packages valid.

### `memgraph`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (4): `libboost-all1.74`, `libgrpc++1`, `libprotobuf32`, `openssl-libs`

### `modsecurity-crs`

**Valid** (2): `ca-certificates`, `libxml2-dev`

**Invalid** (6): `curl-openssl-dev`, `libapache2-mod-security2`, `libgeoip-dev`, `libmodsecurity3`, `libpcre3-dev`,
`libyajl-dev`

### `mongodb`

**Valid** (1): `ca-certificates`

**Invalid** (1): `mongodb-org`

### `mongodb-5`

**Valid** (1): `ca-certificates`

**Invalid** (1): `openssl-libs`

### `mongodb-6`

**Valid** (1): `ca-certificates`

**Invalid** (1): `mongodb-org`

### `mongodb-7`

**Valid** (1): `ca-certificates`

**Invalid** (1): `openssl-libs`

### `mongodb-community`

**Valid** (1): `ca-certificates`

**Invalid** (1): `openssl-libs`

### `mongodb-opsmanager`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `mosquito`

**Valid** (2): `ca-certificates`, `mosquitto-clients`

All packages valid.

### `mosquitto`

**Valid** (2): `ca-certificates`, `mosquitto`

All packages valid.

### `mosquitto-dev`

**Valid** (3): `ca-certificates`, `mosquitto`, `mosquitto-clients`

All packages valid.

### `mozilla-hubs`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `musl`

**Invalid** (1): `musl-dev`

### `mysql`

**Valid** (1): `ca-certificates`

**Invalid** (1): `default-php84-mysql-server`

### `mysql-8`

**Valid** (3): `ca-certificates`, `gnupg`, `psmisc`

**Invalid** (4): `libaio1t64`, `libmecab2`, `libnuma1`, `lsb-release`

### `mysql-anonymizer`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

**Invalid** (1): `default-php84-mysql-client`

### `mysql-backup`

**Valid** (1): `ca-certificates`

**Invalid** (2): `default-php84-mysql-client`, `xz-utils`

### `mysql-init`

**Valid** (1): `ca-certificates`

**Invalid** (1): `default-php84-mysql-client`

### `mysql-restore`

**Valid** (1): `ca-certificates`

**Invalid** (2): `default-php84-mysql-client`, `xz-utils`

### `n8n-nodes`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `n8n-webhook`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `neo4j-admin`

**Invalid** (1): `java-17-runtime`

### `neo4j-enterprise`

**Invalid** (1): `java-17-runtime`

### `neo4j-import`

**Invalid** (1): `java-17-runtime`

### `nextcloud`

**Valid** (4): `ca-certificates`, `nginx`, `sqlite-libs`, `zip`

**Invalid** (8): `php84`, `php84-curl`, `php84-fpm`, `php84-gd`, `php84-intl`, `php84-mbstring`, `php84-mysql`,
`php84-xml`

### `nextcloud-alpine`

**Valid** (4): `ca-certificates`, `nginx`, `sqlite-libs`, `zip`

**Invalid** (8): `php84`, `php84-curl`, `php84-fpm`, `php84-gd`, `php84-intl`, `php84-mbstring`, `php84-mysql`,
`php84-xml`

### `nextcloud-external`

**Valid** (4): `ca-certificates`, `nginx`, `sqlite-libs`, `zip`

**Invalid** (8): `php84`, `php84-curl`, `php84-fpm`, `php84-gd`, `php84-intl`, `php84-mbstring`, `php84-mysql`,
`php84-xml`

### `nextcloud-imaging`

**Valid** (4): `ca-certificates`, `nginx`, `sqlite-libs`, `zip`

**Invalid** (9): `imagick`, `php84`, `php84-curl`, `php84-fpm`, `php84-gd`, `php84-intl`, `php84-mbstring`,
`php84-mysql`, `php84-xml`

### `nextcloud-nginx`

**Valid** (4): `ca-certificates`, `nginx`, `sqlite-libs`, `zip`

**Invalid** (8): `php84`, `php84-curl`, `php84-fpm`, `php84-gd`, `php84-intl`, `php84-mbstring`, `php84-mysql`,
`php84-xml`

### `nginx-alpine`

**Valid** (1): `ca-certificates`

**Invalid** (3): `libpcre3`, `libz1`, `openssl-libs`

### `nginx-cache`

**Valid** (1): `ca-certificates`

**Invalid** (3): `libpcre3`, `libz1`, `openssl-libs`

### `nginx-modsec`

**Valid** (2): `ca-certificates`, `libxml2`

**Invalid** (5): `libgeoip1`, `libpcre3`, `libyajl2`, `libz1`, `openssl-libs`

### `nheko`

**Valid** (2): `ca-certificates`, `glib`

**Invalid** (10): `libcjson4`, `libgl1`, `libqt6core6`, `libqt6gui6`, `libqt6multimedia6`, `libqt6network6`,
`libqt6qml6`, `libqt6quick6`, `libqt6widgets6`, `openssl-libs`

### `nifi-registry`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `node`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `node-red`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `node-red-admin`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `npm-audit`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `nxlog`

**Valid** (4): `ca-certificates`, `expat`, `libzstd1`, `zlib`

**Invalid** (2): `liblzma5`, `openssl-libs`

### `ocserv`

**Valid** (1): `ca-certificates`

**Invalid** (8): `libgmp10`, `libgnutls30`, `libhogweed6`, `libnettle8`, `libpam0g`, `libseccomp2`, `libtasn1-6`,
`libwrap0`

### `onlyoffice-communityserver`

**Valid** (2): `ca-certificates`, `gnupg`

**Invalid** (1): `apt-transport-https`

### `onlyoffice-controlpanel`

**Valid** (2): `ca-certificates`, `gnupg`

**Invalid** (1): `apt-transport-https`

### `onlyoffice-documentserver`

**Valid** (2): `ca-certificates`, `gnupg`

**Invalid** (1): `apt-transport-https`

### `onlyoffice-documentserver-ee`

**Valid** (2): `ca-certificates`, `gnupg`

**Invalid** (1): `apt-transport-https`

### `open-webui`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `open-webui-api`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `openhab3`

**Valid** (2): `ca-certificates`, `libffi-dev`

**Invalid** (2): `java-17-runtime`, `libusb-1.0-0`

### `openjdk`

**Valid** (3): `ca-certificates`, `fontconfig`, `freetype`

All packages valid.

### `openjdk-alpine`

**Valid** (1): `ca-certificates`

**Invalid** (1): `temurin-21-jre-headless`

### `openldap-backup`

**Valid** (2): `ca-certificates`, `coreutils`

**Invalid** (2): `ldap-utils`, `slapd`

### `openldap-lambda`

**Valid** (1): `ca-certificates`

**Invalid** (2): `ldap-utils`, `libsasl2-modules`

### `openproject`

**Valid** (2): `ca-certificates`, `sqlite-libs`

**Invalid** (3): `libmariadb3`, `postgresql-libs`, `ruby3.1`

### `openscap`

**Valid** (2): `ca-certificates`, `scap-security-guide`

**Invalid** (2): `libopenscap8`, `openscap-utils`

### `opensearch`

**Valid** (2): `ca-certificates`, `gosu`

**Invalid** (1): `java-17-runtime`

### `openvpn`

**Valid** (1): `openvpn`

All packages valid.

### `openvpn-as`

**Valid** (7): `ca-certificates`, `iproute2`, `iptables`, `kmod`, `liblz4-1`, `net-tools`, `python3`

**Invalid** (3): `liblzo2-2`, `libpkcs11-helper1`, `openssl-libs`

### `oracledb-xe`

**Valid** (3): `bc`, `ca-certificates`, `netcat-openbsd`

**Invalid** (1): `libaio1`

### `organizer`

**Valid** (3): `ca-certificates`, `nginx`, `nodejs`

**Invalid** (2): `php84-fpm`, `php84-sqlite-libs`

### `orientdb`

**Invalid** (1): `java-17-runtime`

### `pairdrop-server`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `paperless-ngx`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `paperless-ngx-gotenberg`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `paperless-ngx-ocr`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `paperless-ngx-tika`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `pdfarranger`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `pdfmixer`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `photoprism-frontend`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `pi-hole`

**Valid** (4): `ca-certificates`, `iproute2`, `iptables`, `procps`

**Invalid** (1): `openssl-libs`

### `pip-audit`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `plex`

**Valid** (5): `ca-certificates`, `expat`, `fontconfig`, `freetype`, `glib`

**Invalid** (8): `libx11-6`, `libxcb1`, `libxdamage1`, `libxext6`, `libxfixes3`, `libxrender1`, `libxss1`, `libxtst6`

### `plex-media-server`

**Valid** (5): `ca-certificates`, `expat`, `fontconfig`, `freetype`, `glib`

**Invalid** (8): `libx11-6`, `libxcb1`, `libxdamage1`, `libxext6`, `libxfixes3`, `libxrender1`, `libxss1`, `libxtst6`

### `pm2`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `postfix`

**Valid** (1): `postfix`

**Invalid** (1): `mailutils`

### `postfix-constrained`

**Valid** (2): `ca-certificates`, `postfix`

All packages valid.

### `postfix-relay`

**Valid** (2): `ca-certificates`, `postfix`

All packages valid.

### `postgis`

**Valid** (1): `ca-certificates`

**Invalid** (1): `postgresql-16-postgis-3`

### `postgres`

**Valid** (2): `ca-certificates`, `postgresql-17`

All packages valid.

### `postgres-backup`

**Valid** (1): `ca-certificates`

**Invalid** (2): `postgresql-client-__VAR__`, `xz-utils`

### `postgres-restore`

**Valid** (1): `ca-certificates`

**Invalid** (2): `postgresql-client-__VAR__`, `xz-utils`

### `postgresql`

**Valid** (2): `ca-certificates`, `postgresql-17`

All packages valid.

### `postgresql-14`

**Valid** (2): `ca-certificates`, `postgresql-14`

All packages valid.

### `postgresql-15`

**Valid** (2): `ca-certificates`, `postgresql-15`

All packages valid.

### `postgresql-16`

**Valid** (2): `ca-certificates`, `postgresql-16`

All packages valid.

### `postgresql-17`

**Valid** (4): `ca-certificates`, `gnupg`, `liblz4-1`, `libzstd1`

**Invalid** (3): `libicu72`, `libreadline8`, `lsb-release`

### `postgresql-anonymizer`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

**Invalid** (2): `postgresql-client-17`, `postgresql-libs`

### `postgresql-init`

**Valid** (1): `ca-certificates`

**Invalid** (1): `postgresql-client-__VAR__`

### `postgresql-patroni`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

**Invalid** (1): `postgresql-libs`

### `postgrey`

**Valid** (1): `postfix`

**Invalid** (1): `postgrey`

### `powerdns-api`

**Valid** (2): `ca-certificates`, `sqlite-libs`

**Invalid** (5): `libboost-filesystem1.74.0`, `libboost-program-options1.74.0`, `libboost-system1.74.0`,
`libboost-thread1.74.0`, `openssl-libs`

### `powerdns-recursor`

**Valid** (1): `ca-certificates`

**Invalid** (6): `libboost-filesystem1.74.0`, `libboost-program-options1.74.0`, `libboost-system1.74.0`,
`libboost-thread1.74.0`, `libluajit-5.1-2`, `openssl-libs`

### `pptpd`

**Valid** (2): `ca-certificates`, `libstdc++`

**Invalid** (2): `libwrap0`, `ppp`

### `privatebin-nginx`

**Valid** (2): `ca-certificates`, `nginx`

**Invalid** (6): `php84`, `php84-curl`, `php84-fpm`, `php84-php84-gd`, `php84-php84-mbstring`, `php84-php84-xml`

### `prowlarr-develop`

**Valid** (1): `ca-certificates`

All packages valid.

### `pulsar-functions`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `pulsar-proxy`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `pydio`

**Valid** (5): `ca-certificates`, `json-c`, `nginx`, `sqlite-libs`, `zip`

**Invalid** (8): `php84`, `php84-curl`, `php84-fpm`, `php84-gd`, `php84-intl`, `php84-mbstring`, `php84-mysql`,
`php84-xml`

### `python`

**Valid** (1): `ca-certificates`

**Invalid** (1): `python3-minimal`

### `qbittorrent-nox`

**Valid** (1): `ca-certificates`

All packages valid.

### `questdb`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `questdb-python`

**Valid** (3): `ca-certificates`, `python3`, `tzdata`

**Invalid** (1): `postgresql-libs`

### `rabbitmq-amqp`

**Valid** (1): `ca-certificates`

**Invalid** (17): `erlang-asn1`, `erlang-base`, `erlang-crypto`, `erlang-eldap`, `erlang-ftp`, `erlang-inets`,
`erlang-mnesia`, `erlang-os-mon`, `erlang-parsetools`, `erlang-public-key`, `erlang-runtime-tools`, `erlang-snmp`,
`erlang-ssl`, `erlang-syntax-tools`, `erlang-tftp`, `erlang-tools`, `erlang-xmerl`

### `rabbitmq-delayed`

**Valid** (1): `ca-certificates`

**Invalid** (17): `erlang-asn1`, `erlang-base`, `erlang-crypto`, `erlang-eldap`, `erlang-ftp`, `erlang-inets`,
`erlang-mnesia`, `erlang-os-mon`, `erlang-parsetools`, `erlang-public-key`, `erlang-runtime-tools`, `erlang-snmp`,
`erlang-ssl`, `erlang-syntax-tools`, `erlang-tftp`, `erlang-tools`, `erlang-xmerl`

### `rabbitmq-federation`

**Valid** (1): `ca-certificates`

**Invalid** (17): `erlang-asn1`, `erlang-base`, `erlang-crypto`, `erlang-eldap`, `erlang-ftp`, `erlang-inets`,
`erlang-mnesia`, `erlang-os-mon`, `erlang-parsetools`, `erlang-public-key`, `erlang-runtime-tools`, `erlang-snmp`,
`erlang-ssl`, `erlang-syntax-tools`, `erlang-tftp`, `erlang-tools`, `erlang-xmerl`

### `rabbitmq-management`

**Valid** (1): `ca-certificates`

**Invalid** (17): `erlang-asn1`, `erlang-base`, `erlang-crypto`, `erlang-eldap`, `erlang-ftp`, `erlang-inets`,
`erlang-mnesia`, `erlang-os-mon`, `erlang-parsetools`, `erlang-public-key`, `erlang-runtime-tools`, `erlang-snmp`,
`erlang-ssl`, `erlang-syntax-tools`, `erlang-tftp`, `erlang-tools`, `erlang-xmerl`

### `rabbitmq-mqtt`

**Valid** (1): `ca-certificates`

**Invalid** (17): `erlang-asn1`, `erlang-base`, `erlang-crypto`, `erlang-eldap`, `erlang-ftp`, `erlang-inets`,
`erlang-mnesia`, `erlang-os-mon`, `erlang-parsetools`, `erlang-public-key`, `erlang-runtime-tools`, `erlang-snmp`,
`erlang-ssl`, `erlang-syntax-tools`, `erlang-tftp`, `erlang-tools`, `erlang-xmerl`

### `rabbitmq-stomp`

**Valid** (1): `ca-certificates`

**Invalid** (17): `erlang-asn1`, `erlang-base`, `erlang-crypto`, `erlang-eldap`, `erlang-ftp`, `erlang-inets`,
`erlang-mnesia`, `erlang-os-mon`, `erlang-parsetools`, `erlang-public-key`, `erlang-runtime-tools`, `erlang-snmp`,
`erlang-ssl`, `erlang-syntax-tools`, `erlang-tftp`, `erlang-tools`, `erlang-xmerl`

### `radarr-develop`

**Valid** (1): `ca-certificates`

All packages valid.

### `rainloop`

**Valid** (1): `ca-certificates`

**Invalid** (7): `php84`, `php84-curl`, `php84-fpm`, `php84-php84-intl`, `php84-php84-mbstring`, `php84-php84-xml`,
`php84-zip`

### `rclone-browser`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `readarr`

**Valid** (1): `ca-certificates`

All packages valid.

### `realm-server`

**Valid** (1): `ca-certificates`

**Invalid** (2): `java-17-runtime`, `mongodb-org-tools`

### `redash`

**Valid** (3): `ca-certificates`, `py3-pip`, `python3`

**Invalid** (1): `postgresql-libs`

### `redis`

**Valid** (1): `ca-certificates`

**Invalid** (1): `redis`

### `redis-6`

**Valid** (1): `ca-certificates`

**Invalid** (1): `redis`

### `redis-7`

**Valid** (1): `ca-certificates`

**Invalid** (1): `redis`

### `redis-cluster`

**Valid** (1): `ca-certificates`

All packages valid.

### `redis-insight`

**Valid** (4): `ca-certificates`, `fontconfig`, `freetype`, `glib`

**Invalid** (22): `libasound2`, `libatk-bridge2.0-0`, `libatk1.0-0`, `libatspi2.0-0`, `libcairo2`, `libcups2`,
`libdbus-1-3`, `libdrm2`, `libgbm1`, `libnspr4`, `libnss3`, `libpango-1.0-0`, `libx11-6`, `libxcomposite1`,
`libxdamage1`, `libxext6`, `libxfixes3`, `libxi6`, `libxkbcommon0`, `libxrandr2`, `libxrender1`, `libxtst6`

### `redis-sentinel`

**Valid** (1): `ca-certificates`

All packages valid.

### `redmine`

**Valid** (2): `ca-certificates`, `sqlite-libs`

**Invalid** (3): `libmariadb3`, `postgresql-libs`, `ruby3.1`

### `renovate`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `renovatebot`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `rethinkdb`

**Valid** (2): `ca-certificates`, `libstdc++`

**Invalid** (2): `libprotobuf32`, `openssl-libs`

### `rkhunter`

**Valid** (1): `ca-certificates`

**Invalid** (1): `rkhunter`

### `rmilter`

**Valid** (2): `ca-certificates`, `libpcre2-8-0`

**Invalid** (1): `libmilter1.0.1`

### `rocketmq`

**Valid** (1): `ca-certificates`

**Invalid** (1): `openjdk-__VAR__-jre-headless`

### `roundcube`

**Valid** (1): `ca-certificates`

**Invalid** (7): `php84`, `php84-curl`, `php84-fpm`, `php84-php84-intl`, `php84-php84-mbstring`, `php84-php84-xml`,
`php84-zip`

### `rowy`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `rspamd`

**Valid** (1): `rspamd`

All packages valid.

### `rsyslog`

**Valid** (2): `ca-certificates`, `rsyslog`

All packages valid.

### `ruby`

**Valid** (2): `ca-certificates`, `ruby`

All packages valid.

### `rust`

**Valid** (2): `ca-certificates`, `rust`

All packages valid.

### `sbt`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `scap-workbench`

**Valid** (1): `ca-certificates`

**Invalid** (1): `scap-workbench`

### `scylladb`

**Valid** (4): `ca-certificates`, `libxml2-utils`, `python3`, `systemd`

All packages valid.

### `seafile`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `seafile-pro`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `searx`

**Valid** (3): `ca-certificates`, `python3`, `tzdata`

All packages valid.

### `searxng-meta`

**Valid** (3): `ca-certificates`, `python3`, `tzdata`

All packages valid.

### `sentry`

**Valid** (8): `build-base`, `ca-certificates`, `libffi-dev`, `libxml2-dev`, `libxslt-dev`, `openssl-dev`, `py3-pip`,
`python3`

**Invalid** (4): `libjpeg-turbo-turbo-dev`, `libyaml-dev`, `postgresql-libs`, `zlib1g-dev`

### `sentry-cron`

**Valid** (8): `build-base`, `ca-certificates`, `libffi-dev`, `libxml2-dev`, `libxslt-dev`, `openssl-dev`, `py3-pip`,
`python3`

**Invalid** (4): `libjpeg-turbo-turbo-dev`, `libyaml-dev`, `postgresql-libs`, `zlib1g-dev`

### `sentry-worker`

**Valid** (8): `build-base`, `ca-certificates`, `libffi-dev`, `libxml2-dev`, `libxslt-dev`, `openssl-dev`, `py3-pip`,
`python3`

**Invalid** (4): `libjpeg-turbo-turbo-dev`, `libyaml-dev`, `postgresql-libs`, `zlib1g-dev`

### `smartdns`

**Valid** (1): `ca-certificates`

**Invalid** (1): `openssl-libs`

### `snyk`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `snyk-agent`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `sonarr-develop`

**Valid** (1): `ca-certificates`

All packages valid.

### `spamassassin`

**Invalid** (2): `spamassassin`, `spamc`

### `splunk-forwarder`

**Valid** (1): `ca-certificates`

**Invalid** (1): `libgomp1`

### `sql-ledger`

**Valid** (3): `apache2`, `ca-certificates`, `perl`

**Invalid** (7): `libapache-dbi-perl`, `libapache2-mod-perl2`, `libcgi-pm-perl`, `libdbd-pg-perl`, `libdbi-perl`,
`libjson-perl`, `libtemplate-perl`

### `sqlcipher`

**Valid** (1): `ca-certificates`

**Invalid** (1): `openssl-libs`

### `sqlite-browser`

**Valid** (2): `ca-certificates`, `sqlite-libs`

**Invalid** (8): `libqscintilla2-qt5-15`, `libqt5core5t64`, `libqt5gui5t64`, `libqt5network5t64`, `libqt5svg5`,
`libqt5widgets5t64`, `libsqlcipher0`, `openssl-libs`

### `sqlpad`

**Valid** (1): `ca-certificates`

All packages valid.

### `stirling-pdf`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `stirling-pdf-core`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `streamlink`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `strongswan`

**Valid** (4): `ca-certificates`, `iproute2`, `iptables`, `kmod`

**Invalid** (2): `libgmp10`, `openssl-libs`

### `subsonic`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `suitecrm`

**Valid** (5): `ca-certificates`, `json-c`, `nginx`, `openssl`, `zip`

**Invalid** (10): `imap`, `php84`, `php84-curl`, `php84-fpm`, `php84-gd`, `php84-intl`, `php84-mbstring`, `php84-mysql`,
`php84-pdo`, `php84-xml`

### `surrealdb-python`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (1): `libpython3.11`

### `synapse`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `synapse-admin`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `synapse-media`

**Valid** (3): `ca-certificates`, `imagemagick`, `python3`

All packages valid.

### `syslog-ng`

**Valid** (1): `ca-certificates`

**Invalid** (1): `syslog-ng-core`

### `taiga`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `taiga-backend`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `taiga-front`

**Valid** (2): `ca-certificates`, `nginx`

All packages valid.

### `tasmota`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `tasmota-js`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `tautulli`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `tautulli-py`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `text-gen-ui`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `tig`

**Valid** (2): `ca-certificates`, `zlib`

**Invalid** (1): `libncurses6`

### `tigergraph`

**Valid** (3): `ca-certificates`, `libstdc++`, `python3`

**Invalid** (1): `openssl-libs`

### `tigergraph-ecosystem`

**Valid** (3): `ca-certificates`, `libstdc++`, `python3`

**Invalid** (1): `openssl-libs`

### `timescaledb`

**Valid** (1): `ca-certificates`

**Invalid** (1): `postgresql-16-timescaledb`

### `tooljet`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `tooljet-client`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `tooljet-server`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `trino`

**Valid** (2): `ca-certificates`, `python3`

**Invalid** (1): `java-17-runtime`

### `tryton`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `unbound-alpine`

**Valid** (2): `ca-certificates`, `expat`

**Invalid** (1): `openssl-libs`

### `valkey`

**Valid** (2): `ca-certificates`, `valkey`

All packages valid.

### `valkey-cluster`

**Valid** (1): `ca-certificates`

All packages valid.

### `vaultwarden-mysql`

**Valid** (1): `ca-certificates`

**Invalid** (1): `libmariadb3`

### `vaultwarden-postgres`

**Valid** (1): `ca-certificates`

**Invalid** (1): `postgresql-libs`

### `vernemq`

**Valid** (2): `ca-certificates`, `procps`

**Invalid** (1): `openssl-libs`

### `virtuoso`

**Valid** (1): `ca-certificates`

**Invalid** (2): `virtuoso-opensource`, `virtuoso-opensource-7`

### `vpn-controller`

**Valid** (4): `ca-certificates`, `iproute2`, `iptables`, `kmod`

**Invalid** (2): `libelf1`, `libmnl0`

### `vtigercrm`

**Valid** (5): `ca-certificates`, `json-c`, `nginx`, `openssl`, `zip`

**Invalid** (10): `php84`, `php84-curl`, `php84-fpm`, `php84-gd`, `php84-intl`, `php84-mbstring`, `php84-mysql`,
`php84-pdo`, `php84-xml`, `soap`

### `wekan`

**Valid** (1): `ca-certificates`

All packages valid.

### `wg-quick`

**Valid** (5): `ca-certificates`, `iproute2`, `iptables`, `kmod`, `wireguard-tools`

All packages valid.

### `whisparr`

**Valid** (1): `ca-certificates`

All packages valid.

### `whoogle`

**Valid** (3): `ca-certificates`, `python3`, `tzdata`

All packages valid.

### `whoogle-search`

**Valid** (3): `ca-certificates`, `python3`, `tzdata`

All packages valid.

### `wled`

**Valid** (2): `ca-certificates`, `python3`

All packages valid.

### `x86_64-unknown-linux-musl`

**Valid** (1): `rust`

**Invalid** (1): `musl-dev`

### `yacy`

**Valid** (1): `ca-certificates`

**Invalid** (1): `java-17-runtime`

### `yarn`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `yarn-audit`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `zeromq`

**Valid** (2): `ca-certificates`, `libstdc++`

**Invalid** (2): `libgcc-s1`, `libsodium23`

### `zerotier`

**Valid** (3): `ca-certificates`, `iproute2`, `libstdc++`

**Invalid** (1): `libgcc-s1`

### `zigbee2mqtt`

**Valid** (2): `ca-certificates`, `nodejs`

All packages valid.

### `zipkin`

**Valid** (2): `ca-certificates`, `tzdata`

All packages valid.

### `zipline`

**Valid** (3): `ca-certificates`, `nodejs`, `python3`

All packages valid.

## Full Valid Package List

`apache2`, `bc`, `build-base`, `ca-certificates`, `clamav`, `clamav-daemon`, `clamav-freshclam`, `containers-common`,
`coreutils`, `dbus`, `expat`, `ffmpeg`, `fontconfig`, `freetype`, `freshclam`, `glib`, `gnupg`, `gosu`, `haproxy`,
`imagemagick`, `inotify-tools`, `iproute2`, `iptables`, `jq`, `json-c`, `kmod`, `libcap`, `libffi-dev`, `libjpeg-turbo`,
`liblz4-1`, `libnghttp2-14`, `libpcre2-8-0`, `libstdc++`, `libxml2`, `libxml2-dev`, `libxml2-utils`, `libxslt-dev`,
`libzstd1`, `mariadb-backup`, `memcached`, `mosquitto`, `mosquitto-clients`, `net-tools`, `netcat-openbsd`, `nginx`,
`nodejs`, `openldap`, `openssh-client`, `openssl`, `openssl-dev`, `openvpn`, `perl`, `php-ldap`, `postfix`,
`postgresql-14`, `postgresql-15`, `postgresql-16`, `postgresql-17`, `postgresql-client`, `procps`, `psmisc`, `py3-pip`,
`python3`, `rspamd`, `rsync`, `rsyslog`, `ruby`, `rust`, `scap-security-guide`, `socat`, `sqlite-libs`, `systemd`,
`tzdata`, `unzip`, `valkey`, `wireguard-tools`, `zip`, `zlib`
