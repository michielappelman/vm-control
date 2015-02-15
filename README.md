vm-control
==========

A selection of scripts consisting of a single script, with potential to grow to
a larger finite amount in the future.

vm-start.py
-----------

Written mainly because [`tugboat`][1] does not support supplying user data in 
the form of a cloudinit config file. Hence the hard requirement of this script 
to supply such a config. This script can use the `tugboat` config file, but does
require you to add a `token` configuration under the `authentication` section
because [`python-digitalocean`][2] uses that instead of an API client key and
secret.

Summarizing, make sure you have at least the following YAML configuration lines
in `~/.tugboat`:

    authentication:
      token: ...
    defaults:
      ssh_key: <identifier num>

[1]: https://github.com/pearkes/tugboat
[2]: https://github.com/koalalorenzo/python-digitalocean
