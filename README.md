1. Start server: make server
1. Start distcc monitor (from a different window): make mon
1. Compile: make [distcc]

`server_one` and `server_two` are made-up names for localhost, with `/etc/hosts` like this:

    127.0.0.1	localhost
    127.0.1.1	fenix
    127.0.1.1 server_one server_two

If `distcc` is working as expected, you should see server_one and server_two in distcc monitor being used for Compile.

This needs distcc version >= 3.3.x

