#mkcert -install
export MY_WIFI_IP=`ifconfig | awk '/inet /&&!/127.0.0.1/{print $2; exit;}'`
mkcert $MY_WIFI_IP localhost 127.0.0.1 ::1

mv $MY_WIFI_IP+3-key.pem key.pem
mv $MY_WIFI_IP+3.pem public.crt

cp key.pem ../client/snowpack.key
cp public.crt ../client/snowpack.crt
