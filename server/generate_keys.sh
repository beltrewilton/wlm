#openssl genrsa -out key.pem 2048
#openssl rsa -in key.pem -outform PEM -pubout -out public.crt

# try this.
#  openssl req -x509 -newkey rsa:2048 -keyout key.pem -out public.crt -days 365

#mkcert -install
mkcert 10.0.0.6 localhost 127.0.0.1 ::1
mv 10.0.0.6+3-key.pem key.pem
mv 10.0.0.6+3.pem public.crt

cp key.pem ../client/snowpack.key
cp public.crt ../client/snowpack.crt
