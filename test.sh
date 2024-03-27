#!/bin/bash
read -p "email:" email
read -sp "password:" pw

echo $emailでログイン

http --session kakuyomu \
     -f https://kakuyomu.jp/login \
        email_address=$email password=$pw \
    X-requested-With:XMLHttpRequest