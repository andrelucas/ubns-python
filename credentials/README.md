# Minimal CA

<!-- vscode-markdown-toc -->
* [Set up the CA](#SetuptheCA)
* [Create cert](#Createcert)
	* [tl;dr](#tldr)
* [Revoke a cert](#Revokeacert)
* [Generate a CRL](#GenerateaCRL)
* [Clean up and start again](#Cleanupandstartagain)

<!-- vscode-markdown-toc-config
	numbering=false
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

This is a toy CA to go with the toy Authenticator implementation.

It is based partly on [this very minimal
CA](https://gist.github.com/drmalex07/7323e2ec8dc104140746f54c76111e2b) with
some modifications. There's no need for something as sophisticated as EasyRSA
here.

## <a name='SetuptheCA'></a>Set up the CA

```sh
cd credentials
./create_ca.sh
```

This will create `root.crt`, and some support files for the toy CA.

## <a name='Createcert'></a>Create cert

### <a name='tldr'></a>tl;dr

Create a cert for localhost. This is often all you need, because you'll note
the cert is marked so it can be used as both a client and a server cert.

```sh
./create_cert.sh -a "extendedKeyUsage = clientAuth,serverAuth" \
	-a "subjectAltName=DNS:localhost,IP:127.0.0.1,IP:::1" \
	localhost localhost
```

This will drop a key in `localhost.key` and a certificate in `localhost.crt`.

Create a cert for this host, saving in file `SHORTHOSTNAME.{crt,key}`, with CN
`LONGHOSTNAME`. For completeness, set the subjectAltName as well - this is a
good idea.

Clearly, this depends on your host having its hostname set
properly; if `$(hostname -f)` doesn't give a fully-qualified domain name, and
`$(hostname -s)` doesn't give a short hostname, then you might have to just
fill in the names manually.

```sh
./create_cert.sh -a "extendedKeyUsage = clientAuth,serverAuth" \
	-a "subjectAltName=DNS:$(hostname -f)" \
	$(hostname -s) $(hostname -f)
```

You could include the IP addresses in the subjectAltName if you feel the
need. Of course, this required working name resolution and the presence of the
dig(1) tool.

```sh
./create_cert.sh -a "extendedKeyUsage = clientAuth,serverAuth" \
	"-a subjectAltName=DNS:$(hostname -f),IP:$(dig +short $(hostname -f))" \
	$(hostname -s) $(hostname -f)
```

More explicit localhost cert:

```sh
./create_cert.sh -a "subjectAltName = DNS:localhost,IP:127.0.0.1" \
	-a "extendedKeyUsage = clientAuth,serverAuth" \
	localhost localhost
```

This will drop a key in `localhost.key` and a certificate in `localhost.crt`,
with subjectAltName set so that a realistic gRPC URI (e.g.
`dns:127.0.0.1:8002`) will work.

You could also have set the CN (the second regular command line parameter) to
'127.0.0.1', but that makes for ugly filenames. Also you shouldn't use the CN
for identity any more, it's deprecated.

The simplest form (not quite enough):

```sh
./create_cert.sh localhost localhost
```

After a few prompts, this creates `localhost.key` and `localhost.crt` which
can be used for the gRPC server. The cert will have CN `localhost`.

If you attempt to create a cert for the same CN, the CA will complain - you
need to revoke the old certificate first. Instructions below.

To create a certificate for host `rhubarb.com` I recommend setting the
subjectAltName as well, just because not every TLS implementation cares about the CN.

```sh
./create_cert.sh -a "subjectAltName = DNS:rhubarb.com" rhubarb rhubarb.com
```

You can add whatever X.509 extensions you like with this syntax:

```sh
./create_cert.sh \
	-a "subjectAltName = DNS:rhubarb.com,DNS:custard.com,IP:127.0.0.1,IP:::1" \
	rhubarb rhubarb.com
```

## <a name='Revokeacert'></a>Revoke a cert

Why is this useful here?

- It might be helpful to be able to recreate certs with
different subjectAltName values, whilst not having to change the root cert
installed on other hosts or in other containers.

- You might want to test the operation of the CRL, in which case it helps to
  have some, well, revoked certs.

```sh
./revoke.sh localhost.crt
```

This will revoke the cert in file `localhost.crt`. If you've lost the file,
you could either just start again (doing the cleanup shown below), or look in
the `certs/` directory where copies of issued certs are kept. To see a text
representation of a cert, do:

```sh
openssl x509 -text -noout -in certs/01.pem
```

## <a name='GenerateaCRL'></a>Generate a CRL

```sh
./gencrl.sh
```

## <a name='Cleanupandstartagain'></a>Clean up and start again

This will reset everything and generate a new CA. Make sure you update your
CA files everywhere or you'll have a bad time.

```sh
./clean.sh
```
