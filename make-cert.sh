# /bin/bash

if [ "$1" = ""  ] || [ "$2" = "" ] ;then
    echo "script for making csrs for dev certs"
    echo "usage: ./make-cert.sh <user> <va|ca>"
    echo "i.e. ./make-cert.sh jdoe ca"
    exit 0
fi

username=$1
homedir=$(whoami)
region="${2}1"
starname="star.${username}.dev-${region}.internal.pos-api.com"
asteriskname="*.${username}.dev-${region}.internal.pos-api.com"
bits=2048
dir="/home/$homedir/certs/dev/$username/"

mkdir -p $dir
cd $dir

echo
echo "making the KEY for $starname"
openssl genrsa -out ${starname}.key $bits >/dev/null 2>&1

echo "making the CSR for $starname"

cat << EOD > expect.cert.sh
#!/usr/bin/expect -f

    set timeout -1
    match_max 100000

    spawn openssl req -new -newkey rsa:$bits -nodes -key ${dir}${starname}.key -out ${dir}${starname}.csr

    expect -exact "Country Name (2 letter code) \[AU\]:"
    send -- "US\r"
    expect -exact "State or Province Name (full name) \[Some-State\]:"
    send -- "California\r"
    expect -exact "Locality Name (eg, city) \[\]:"
    send -- "San Francisco\r"
    expect -exact "Organization Name (eg, company) \[Internet Widgits Pty Ltd\]:"
    send -- "Omnivore Technologies, Inc.\r"
    expect -exact "Organizational Unit Name (eg, section) \[\]:"
    send -- "Department of SSL Tomfoolery\r"
    expect -exact "Common Name (e.g. server FQDN or YOUR name) \[\]:"
    send -- "$asteriskname"
    expect ".internal.pos-api.com"
    send -- "\r"
    expect -exact "Email Address \[\]:"
    send -- "corporate@omnivore.io\r"
    expect -exact "A challenge password \[\]:"
    send -- "\r"
    expect -exact "An optional company name \[\]:"
    send -- "\r"
    expect eof
EOD
chmod u+x expect.cert.sh
./expect.cert.sh >/dev/null

rm -f expect.cert.sh

echo "created ${starname}.key and ${starname}.csr"

keysum=$(openssl rsa -noout -modulus -in ${dir}${starname}.key | openssl md5 | awk '{print $NF}')
csrsum=$(openssl req -noout -modulus -in ${dir}${starname}.csr | openssl md5 | awk '{print $NF}')

if [ "$keysum" != "$csrsum" ] ;then
    echo "something went wrong; the CSR and key don't match"
    exit 1
fi

echo "everything checks out, here's the csr:" 
echo
cat ${dir}${starname}.csr 
echo
exit 0

