
Setup steps:

To speed up amass add more resolvers (default is 8, 25 is recommended)

https://github.com/vortexau/dnsvalidator

`sort -R resolvers.txt | tail -n25 > 25resolvers.txt`

Create Gmail account and enable insecure applciations.

Copy subConfig.ini.default to config.ini and update required settings (probably just email addresses and passwords)

Copy amass_config.ini.default to amass_config.ini and specify any changes you want to make.
