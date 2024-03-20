# README.md for ubns-python

<!-- vscode-markdown-toc -->

<!-- vscode-markdown-toc-config
	numbering=false
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

This is a simple server and client used to test the RGW implementation of
UBNS.

## Setup

### Python

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


### Dependencies for working with gRPC files.

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

### `buf`

```sh
$ go install github.com/bufbuild/buf/cmd/buf@v1.30.0
$ which bug
/home/myuser/go/bin/buf
```

You have to have `~/go/bin` in your PATH for this to work. If it doesn't
install to `~/go/bin`, you've changed GOPATH, and you probably know how to
sort this out for yourself.

## Running

### Running the server

```sh
$ ./ubns_server.py
```

XXX
