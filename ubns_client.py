#!/usr/bin/env python3
"""
Simple test client for the AuthService gRPC protocol.
"""

import argparse
import base64
from google.rpc import code_pb2
from google.rpc import error_details_pb2
from google.rpc import status_pb2
import grpc
from grpc_status import rpc_status
import logging
import os
import sys

from ubdb.v1 import ubdb_pb2_grpc
from ubdb.v1 import ubdb_pb2


def unpack_grpc_error(e: grpc.RpcError):
    status = rpc_status.from_call(e)
    if status is None:
        logging.error(f"RPC failed: {e}")
    else:
        logging.error(
            f"RPC failed: error={e} code={status.code} message='{status.details}'"
        )
        for detail in status.details:
            # Unpack the ANY if it's a specific type.
            if detail.Is(ubdb_pb2.S3ErrorDetails.DESCRIPTOR):
                s3_error = ubdb_pb2.S3ErrorDetails()
                detail.Unpack(s3_error)
                tstr = ubdb_pb2.S3ErrorDetails.Type.DESCRIPTOR.values_by_number[
                    s3_error.type
                ].name  # String form of the S3 error type.
                logging.error(
                    f"S3ErrorDetails: type={tstr} http_status_code={s3_error.http_status_code}"
                )


def add(stub: ubdb_pb2_grpc.UBDBServiceStub, args):
    req = ubdb_pb2.AddBucketEntryRequest()
    req.bucket = args.bucket
    req.owner = args.owner
    req.cluster = args.cluster

    try:
        response: ubdb_pb2.AddBucketResponse = stub.AddBucketEntry(req)
        logging.info(f"server response: {response}")
        return True

    except grpc.RpcError as e:
        unpack_grpc_error(e)
        return False


def delete(stub: ubdb_pb2_grpc.UBDBServiceStub, args):
    req = ubdb_pb2.DeleteBucketEntryRequest()
    req.bucket = args.bucket
    req.cluster = args.cluster
    try:
        response: ubdb_pb2.DeleteBucketResponse = stub.DeleteBucketEntry(req)
        logging.info(f"server response: {response}")
        return True

    except grpc.RpcError as e:
        unpack_grpc_error(e)
        return False


def update(stub: ubdb_pb2_grpc.UBDBServiceStub, args):
    req = ubdb_pb2.UpdateBucketEntryRequest()
    req.bucket = args.bucket
    req.cluster = args.cluster
    if args.update_state == "created":
        req.state = ubdb_pb2.BucketState.BUCKET_STATE_CREATED
    elif args.update_state == "deleting":
        req.state = ubdb_pb2.BucketState.BUCKET_STATE_DELETING
    else:
        logging.error(f"Unknown state '{args.state}'")
        return False

    try:
        response: ubdb_pb2.UpdateBucketEntryResponse = stub.UpdateBucketEntry(req)
        logging.info(f"server response: {response}")
        return True

    except grpc.RpcError as e:
        unpack_grpc_error(e)
        return False


def issue(channel, args):
    """
    Issue the RPC. Factored out so we can use different types of channel.
    """
    stub = ubdb_pb2_grpc.UBDBServiceStub(channel)

    if args.command == "add":
        success = add(stub, args)
    elif args.command == "delete":
        success = delete(stub, args)
    elif args.command == "update":
        success = update(stub, args)
    else:
        logging.error(f"Unknown command '{args.command}'")
        sys.exit(2)


def _load_credential_from_file(filepath):
    """https://github.com/grpc/grpc/blob/master/examples/python/auth/_credentials.py"""
    real_path = os.path.join(os.path.dirname(__file__), filepath)
    with open(real_path, "rb") as f:
        return f.read()


def main(argv):
    p = argparse.ArgumentParser(description="AuthService client")
    p.add_argument(
        "command", help="command to run", choices=["add", "delete", "update"]
    )
    p.add_argument("--bucket", help="bucket name", required=True)
    p.add_argument(
        "-t", "--tls", help="connect to the server using TLS", action="store_true"
    )
    p.add_argument("--uri", help="server uri (will override address and port!)")
    p.add_argument("-a", "--address", help="server address", default="127.0.0.1")
    p.add_argument("-p", "--port", type=int, default=9000, help="server listen port")
    p.add_argument("-v", "--verbose", action="store_true")

    p.add_argument("-o", "--owner", help="owner of the bucket")
    p.add_argument("-c", "--cluster", help="client cluster ID")
    p.add_argument(
        "-s",
        "--update-state",
        choices=["created", "deleting"],
        help="update state of the bucket",
    )

    ptls = p.add_argument_group("TLS arguments")
    ptls.add_argument("--ca-cert", help="CA certificate file")
    ptls.add_argument("--client-cert", help="client certificate file (NOT YET USED)")
    ptls.add_argument("--client-key", help="client key file (NOT YET USED)")

    args = p.parse_args(argv)
    if not args.command:
        p.usage()
        sys.exit(1)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.tls:
        if not args.ca_cert:
            logging.error("TLS requires a CA certificate")
            sys.exit(1)

    # Set up a channel string first.
    server_address = f"dns:{args.address}:{args.port}"
    if args.uri:
        server_address = args.uri
    logging.debug(f"using server_address {server_address}")
    success = False

    if args.command:
        if args.command == "add":
            if not args.owner:
                logging.error("add command requires an owner")
                sys.exit(1)
            if not args.cluster:
                logging.error("add command requires a cluster")
                sys.exit(1)

        elif args.command == "delete":
            if not args.cluster:
                logging.error("delete command requires a cluster")
                sys.exit(1)

        elif args.command == "update":
            if not args.cluster:
                logging.error("update command requires a cluster")
                sys.exit(1)
            if not args.update_state:
                logging.error("update command requires an update state")
                sys.exit(1)

        else:
            logging.error(f"Unknown command '{args.command}'")
            sys.exit(1)

    if args.tls:
        root_crt = _load_credential_from_file(args.ca_cert)
        channel_credential = grpc.ssl_channel_credentials(root_crt)
        with grpc.secure_channel(server_address, channel_credential) as channel:
            issue(channel, args)
    else:
        with grpc.insecure_channel(server_address) as channel:
            issue(channel, args)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
