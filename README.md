# Token Reverser
Words list generator to crack security tokens.

## Installation
```
$ git clone https://github.com/dariusztytko/token-reverser.git
```

## Example use case
1. You are testing reset password function
1. Reset password token was sent to your email box (e.g. 582431d4c7b57cb4a3570041ffeb7e10)
1. You suppose, it is a md5 hash of the data you provided on registration
1. On registration you entered the following data:
    * First name: Foo
    * Last name: Bar
    * Email: foo.bar@example.com
    * Birth date: 1985-05-23
    * Phone: 202-555-0185
    * Address: 3634 Forest Drive
1. In addition, you have an access to the following extra data:
    * Application user ID: 74824
    * Date of the reset password HTTP request ("Date" response header): Tue, 10 Mar 2020 17:12:59 GMT
1. Use Token Reverser to generate words list from the known data:
    ```
    python3 token-reverser.py --date "Tue, 10 Mar 2020 17:12:59 GMT" Foo Bar foo.bar@example.com 1985-05-23 202-555-0185 "3634 Forest Drive" 74824 > words
    ```

1. Use hashcat to crack reset password token:
    ```
    hashcat64.exe -m 0 582431d4c7b57cb4a3570041ffeb7e10 words
    hashcat (v5.1.0) starting...
    [...]

    582431d4c7b57cb4a3570041ffeb7e10:74824!Foo!Bar!foo.bar@example.com!1583860379

    Session..........: hashcat
    Status...........: Cracked
    Hash.Type........: MD5
    Hash.Target......: 582431d4c7b57cb4a3570041ffeb7e10
    [...]
    ```

1. Now you know that reset password tokens are generated as follows:
    ```
    md5(user ID!first name!last name!email!current timestamp)
    ```

## Usage
```
usage: token-reverser.py [-h] [-d DATE] [-o TIMESTAMP_OFFSET] [-s SEPARATORS]
                         data [data ...]

Words list generator to crack security tokens v1.2

positional arguments:
  data                  data chunks

optional arguments:
  -h, --help            show this help message and exit
  -d DATE, --date DATE  timestamp from this date will be used as an additional
                        data chunk, example: Tue, 10 Mar 2020 14:06:36 GMT
  -o TIMESTAMP_OFFSET, --timestamp-offset TIMESTAMP_OFFSET
                        how many previous (to timestamp from date) timestamps
                        should be used as an additional data chunks, default: 1
  -s SEPARATORS, --separators SEPARATORS
                        data chunks separators to check, default:
                        ~`!@#$%^&*()_+-={}|[]\:";'<>?,./ \t
```

## Changes
Please see the [CHANGELOG](CHANGELOG)
