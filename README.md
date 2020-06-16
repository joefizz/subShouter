
This little script is basically a wrapper for amass.  It will run `amass enum` on all the root domains for your configured programs, followed by `amass track` to identify those subdomains that are new.  The new subdomains will then be emailed to you.


Setup steps:

amass has default resolvers but we can add more to speed up the process, before running subShouter ensure you create/update the DNS resolvers list by running `./subShouter.py dns`

Create Gmail account and enable insecure applications (https://myaccount.google.com/lesssecureapps).

`cp subConfig.ini.default subConfig.ini` and update required settings (probably just email addresses and passwords)

`cp amass_config.ini.default amass_config.ini` and specify any changes you want to make. This is specifcally for amass


Features:

`enum` - starts amass and enumerates all the root domains stored with programs. tracks the changes and sends email alerting to all subdomain changes.

`add` - adds a new program to the enumeration task.  list of programs is stored in `programs.txt`.  amass data for programs is stored separately for each one in the ./programs/ folder. Once a programs is added the root domains should be added to the domains.txt file in the programs folder.

`delete` - deletes a program from the programs.txt file but leaves the program folder intact.

`purge` - deletes folders for all programs that are NOT in the programs.txt file.

`dns` - updates the list of DNS resolvers used by amass.

Example:

```
./subShouter.py dns
./subShouter.py add verizon
echo verizon.com > ./programs/verizon/domains.txt
./subShouter.py enum
```
