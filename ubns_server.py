#!/usr/bin/env python3
"""
Minimal HTTP server implementing the UBNS protocol.

Usage::
    ./ubns_server.py [<port>]
"""

import argparse
from concurrent import futures
from google.protobuf import any_pb2
from google.rpc import code_pb2
from google.rpc import error_details_pb2
from google.rpc import status_pb2
import grpc
from grpc_status import rpc_status
import logging
import re
import os
import sys

from ubdb.v1 import ubdb_pb2_grpc
from ubdb.v1 import ubdb_pb2

class BucketNotFoundError(Exception):
    def __init__(self, bucket):
        super().__init__(f"bucket '{bucket}' not found")

class BucketAlreadyExistsError(Exception):
    def __init__(self, bucket):
        super().__init__(f"bucket '{bucket}' already exists")

class BucketNameDatabase:

    def __init__(self):
        self.buckets = set()

    def add_bucket(self, bucket_name):
        if bucket_name in self.buckets:
            raise BucketAlreadyExistsError(bucket_name)
        self.buckets.add(bucket_name)

    def delete_bucket(self, bucket_name):
        try:
            self.buckets.remove(bucket_name)
        except KeyError:
            raise BucketNotFoundError(bucket_name)

    def update_bucket(self, bucket_name, new_name):
        if bucket_name not in self.buckets:
            raise BucketNotFoundError(bucket_name)
        raise Exception("not implemented")

class UBDBServer(ubdb_pb2_grpc.UBDBServiceServicer):

    def __init__(self):
        self.db = BucketNameDatabase()

    def set_context_error(self, context, e: Exception):
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        context.set_details(str(e))
        return

    def AddBucketEntry(self, request, context):
        logging.info(f"AddBucketEntry: {request}")
        try:
            self.db.add_bucket(request.bucket)
            return ubdb_pb2.AddBucketEntryResponse()
        except BucketAlreadyExistsError as e:
            self.set_context_error(context, e)
            return ubdb_pb2.AddBucketEntryResponse()

    def DeleteBucketEntry(self, request, context):
        logging.info(f"DeleteBucketEntry: {request}")
        try:
            self.db.delete_bucket(request.bucket)
            return ubdb_pb2.DeleteBucketEntryResponse()
        except BucketNotFoundError as e:
            self.set_context_error(context, e)
            return ubdb_pb2.DeleteBucketEntryResponse()


    def UpdateBucketEntry(self, request, context):
        logging.info(f"UpdateBucketEntry: {request}")
        try:
            self.db.update_bucket(request.bucket)
            return ubdb_pb2.UpdateBucketEntryResponse()
        except BucketNotFoundError as e:
            self.set_context_error(context, e)
            return ubdb_pb2.UpdateBucketEntryResponse()


def _load_credential_from_file(filepath):
    """https://github.com/grpc/grpc/blob/master/examples/python/auth/_credentials.py"""
    real_path = os.path.join(os.path.dirname(__file__), filepath)
    with open(real_path, "rb") as f:
        return f.read()


def run(args):
    server_address = f"127.0.0.1:{args.port}"
    logging.info("Starting gRPC service...\n")
    try:
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10),
            options=(
                ("grpc.so_reuseport", 0),
            ),  # This apparently helps detect port reuse - see https://github.com/grpc/grpc/issues/16920
        )
        ubdb_pb2_grpc.add_UBDBServiceServicer_to_server(UBDBServer(), server)

        if args.tls:
            server_crt = _load_credential_from_file(args.server_cert)
            server_key = _load_credential_from_file(args.server_key)
            server_credentials = grpc.ssl_server_credentials(
                (
                    (
                        server_key,
                        server_crt,
                    ),
                )
            )
            server.add_secure_port(server_address, server_credentials)

        else:
            server.add_insecure_port(server_address)

        server.start()
        logging.info(f"Server started, listening on {server_address}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass
    logging.info("Stopping gRPC server...\n")


if __name__ == "__main__":
    from sys import argv

    p = argparse.ArgumentParser(description="Auth gRPC server")
    p.add_argument("port", type=int, help="Listen port", nargs="?", default=9000)
    p.add_argument(
        "-t", "--tls", help="connect to the server using TLS", action="store_true"
    )
    p.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    ptls = p.add_argument_group("TLS arguments")
    ptls.add_argument("--ca-cert", help="CA certificate file (NOT YET USED)")
    ptls.add_argument("--server-cert", help="client certificate file")
    ptls.add_argument("--server-key", help="client key file")

    args = p.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.tls:
        if not args.server_cert:
            logging.error("TLS requires a server certificate")
            sys.exit(1)
        if not args.server_key:
            logging.error("TLS requires a server key")
            sys.exit(1)

    run(args)
