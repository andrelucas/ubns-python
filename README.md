# README.md for ubns-python

<!-- vscode-markdown-toc -->
* [Setup](#Setup)
	* [Python](#Python)
	* [Dependencies for working with gRPC files.](#DependenciesforworkingwithgRPCfiles.)
	* [`buf`](#buf)
* [Running](#Running)
	* [Running the server](#Runningtheserver)
	* [Running the server with mTLS](#RunningtheserverwithmTLS)
	* [Running the client](#Runningtheclient)

<!-- vscode-markdown-toc-config
	numbering=false
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

This is a simple server and client used to test the RGW implementation of
UBNS.

## <a name='Setup'></a>Setup

### <a name='Python'></a>Python

If you don't care about installing system stuff, you can YOLO it:

```sh
$ sudo pip3 install grpcio grpcio-status grpcio-tools
```

A more reasoned approach, and what a more recent Python is likely to steer you
towards, is using a virtual env:

```sh
$ virtualenv ~/venv-grpc
$ source ~/venv-grpc/bin/activate
(venv-grpc) > $ pip3 install grpcio grpcio-status grpcio-tools
...
```

As long as you're in this venv, the packages will be present.


### <a name='DependenciesforworkingwithgRPCfiles.'></a>Dependencies for working with gRPC files.

You don't need this to run the programs, only to change the Python generated
code if the .proto file(s) change.

In order to update the gRPC sources, you need `grpc_python_plugin` and
`protoc` for `buf`, a tool used by gen2 to work with protobuf in order to save
everyone time and effort.

On macOS:

```sh
$ brew install grpc
$ hash -r
$ which grpc_python_plugin
/opt/homebrew/bin/grpc_python_plugin
```

On Linux, unbelievably, you need to install it from source. If you're
developing on Ceph (and you probably are), it will be installed in
/usr/local/grpc/bin as part of the binary dependency installation, along with
the `protoc` binary. Just add it to PATH.

```sh
$ export PATH=/usr/local/grpc/bin:$PATH
$ which grpc_python_plugin
/usr/local/grpc/bin/grpc_python_plugin
```

### <a name='buf'></a>`buf`

```sh
$ go install github.com/bufbuild/buf/cmd/buf@v1.30.0
$ which buf
/home/myuser/go/bin/buf
```

You have to have `~/go/bin` in your PATH for this to work. If it doesn't
install to `~/go/bin`, you've changed GOPATH, and you probably know how to
sort this out for yourself.

## <a name='Running'></a>Running

### <a name='Runningtheserver'></a>Running the server

```sh
$ ./ubns_server.py
```

You can specify the address and port if you need to:

```sh
$ ./ubns_server 0.0.0.0 8000
```

### <a name='RunningtheserverwithmTLS'></a>Running the server with mTLS

Assuming you're not bringing your own certificates, you need to have set up
the CA; see [the credentials README](credentials/README.md).

If you are bringing your own certs and keys, save yourself some time by making
sure they're not using sha1 digests. This will not work with even slightly
recent C++ gRPC.

For a server for localhost only, once you have localhost.crt and localhost.key
set up:

```sh
./ubns_server.py ./ubns_server.py -t -v \
        --ca-cert credentials/root.crt \
        --server-cert credentials/localhost.crt \
        --server-key credentials/localhost.key
```

For a non-localhost server:

```sh
./ubns_server.py -v --tls \
        --ca-cert credentials/root.crt \
        --server-cert credentials/MYHOSTNAME.crt \
        --server-key credentials/MYHOSTNAME.key
```

This requires MYHOSTNAME.crt and MYHOSTNAME.key set up as directed,
and for name resolution to be working properly.

### <a name='Runningtheclient'></a>Running the client

```sh
# Add a bucket.
$ ./ubns_client.py add --bucket foo
INFO:root:server response:

# Adding it again will fail.
$ ./ubns_client.py add --bucket foo
ERROR:root:RPC failed: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.INVALID_ARGUMENT
        details = "bucket 'foo' already exists"
        debug_error_string = "UNKNOWN:Error received from peer ipv4:127.0.0.1:9000 {created_time:"2024-03-20T12:49:22.212626+00:00", grpc_status:3, grpc_message:"bucket \'foo\' already exists"}"
>

# Update the bucket to the CREATED state (necessary to complete creation).
$ ./ubns_client.py --bucket foo --cluster bar --update-state created update
INFO:root:server response:

# Update the bucket to the DELETING state (necessary to begin deletion).
$ ./ubns_client.py --bucket foo --cluster bar --update-state deleting update
INFO:root:server response:

# Delete the bucket.
$ ./ubns_client.py delete --bucket foo --cluster bar
INFO:root:server response:

# Re-deleting the bucket won't work.
$ ./ubns_client.py delete --bucket foo --cluster bar
ERROR:root:RPC failed: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.INVALID_ARGUMENT
        details = "bucket 'foo' not found"
        debug_error_string = "UNKNOWN:Error received from peer ipv4:127.0.0.1:9000 {created_time:"2024-03-20T12:50:49.842862+00:00", grpc_status:3, grpc_message:"bucket \'foo\' not found"}"
>
```

### Running the client with TLS

This is the same as above, with a bunch of additional options:

```sh
# If you forget the TLS options, you'll get this:
$ ./ubns_client.py --bucket foo --cluster bar --owner baz add
ERROR:root:RPC failed: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.UNAVAILABLE
        details = "failed to connect to all addresses; last error: UNAVAILABLE: ipv4:127.0.0.1:9000: Socket closed"
        debug_error_string = "UNKNOWN:Error received from peer  {created_time:"2024-04-17T10:10:40.882798426+00:00", grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNAVAILABLE: ipv4:127.0.0.1:9000: Socket closed"}"
>

# With the necessary options.
$ ./ubns_client.py --tls \
        --ca-cert credentials/root.crt \
        --client-cert credentials/localhost.crt \
        --client-key credentials/localhost.key \
        --bucket foo --cluster bar --owner baz add
INFO:root:server response:

# You get the idea.
```
