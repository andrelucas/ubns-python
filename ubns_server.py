#!/usr/bin/env python3
"""
Minimal HTTP server implementing the UBNS protocol.

Usage::
    ./ubns_server.py [<port>]
"""

import argparse
from concurrent import futures
from enum import Enum
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


class BucketDeleteWhenNotInDeletingState(Exception):
    def __init__(self, bucket):
        super().__init__(f"bucket '{bucket}' is not in the DELETING state for deletion")


class MismatchedClusterError(Exception):
    def __init__(self, bucket, cluster):
        super().__init__(
            f"bucket '{bucket}' cluster '{cluster}' does not match existing cluster '{cluster}'"
        )


class BucketState(Enum):
    NONE = 0
    CREATING = 1
    CREATED = 2
    DELETING = 3
    DELETED = 4


class Bucket:
    def __init__(self, name, owner, cluster):
        self.name = name
        self.owner = owner
        self.cluster = cluster
        self.state = BucketState.NONE

    def state(self):
        return self.state

    def owner(self):
        return self.owner

    def cluster(self):
        return self.cluster

    def __str__(self):
        return f"Bucket(name={self.name}, owner={self.owner}, cluster={self.cluster}, state={self.state})"


class BucketNameDatabase:

    def __init__(self):
        self.buckets: dict[str, Bucket] = {}

    def add_bucket(self, bucket_name, owner, cluster):
        if bucket_name in self.buckets:
            logging.error(f"Bucket '{bucket_name}' already exists")
            raise BucketAlreadyExistsError(bucket_name)

        bucket = Bucket(bucket_name, owner, cluster)
        logging.info(f"add_bucket: new bucket={bucket_name}")

        self.buckets[bucket_name] = bucket
        self.buckets[bucket_name].state = BucketState.CREATING
        logging.info(f"Added bucket: {self.buckets[bucket_name]}")

    def delete_bucket(self, bucket_name: str, cluster: str):
        if bucket_name not in self.buckets:
            logging.error(f"Bucket '{bucket_name}' not found")
            raise BucketNotFoundError(bucket_name)

        bucket = self.buckets[bucket_name]
        logging.info(f"delete_bucket: current bucket={bucket}")

        if bucket.cluster != cluster:
            logging.error(
                f"Cluster '{cluster}' does not match existing cluster '{bucket.cluster}'"
            )
            raise MismatchedClusterError(bucket_name, cluster)

        if bucket.state != BucketState.DELETING:
            msg = "bucket '{bucket_name}' is not in the DELETING state"
            logging.error(msg)
            raise Exception(msg)

        logging.info(f"Deleting bucket: {self.buckets[bucket_name]}")
        del self.buckets[bucket_name]

    def update_bucket(self, bucket_name: str, cluster: str, state: str):
        if bucket_name not in self.buckets:
            logging.error(f"Bucket '{bucket_name}' not found")
            raise BucketNotFoundError(bucket_name)

        bucket = self.buckets[bucket_name]
        logging.info(f"update_bucket: current bucket={bucket}")

        if bucket.cluster != cluster:
            logging.error(
                f"Cluster '{cluster}' does not match existing cluster '{bucket.cluster}'"
            )
            raise MismatchedClusterError(bucket_name, cluster)

        if state == BucketState.CREATED:
            if bucket.state != BucketState.CREATING:
                msg = f"bucket '{bucket_name}' is not in the CREATING state for CREATED update"
                logging.error(msg)
                raise Exception(msg)
            else:
                bucket.state = BucketState.CREATED
                logging.info(f"Updated bucket: {self.buckets[bucket_name]}")
        elif state == BucketState.DELETING:
            if bucket.state != BucketState.CREATED:
                msg = f"bucket '{bucket_name}' is not in the CREATED state for DELETING update"
                logging.error(msg)
                raise Exception(msg)
            else:
                bucket.state = BucketState.DELETING
                logging.info(f"Updated bucket: {self.buckets[bucket_name]}")
        else:
            raise Exception(f"Unknown state '{state}'")


class UBDBServer(ubdb_pb2_grpc.UBDBServiceServicer):

    def __init__(self):
        self.db = BucketNameDatabase()

    def set_context_error(self, context, e: Exception):
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        context.set_details(str(e))
        return

    def AddBucketEntry(self, request, context):
        logging.info(
            f"received: AddBucketEntry: bucket={request.bucket} owner={request.owner} cluster={request.cluster}"
        )
        try:
            self.db.add_bucket(request.bucket, request.owner, request.cluster)
            return ubdb_pb2.AddBucketEntryResponse()
        except Exception as e:
            self.set_context_error(context, e)
            return ubdb_pb2.AddBucketEntryResponse()

    def DeleteBucketEntry(self, request, context):
        logging.info(
            f"received: DeleteBucketEntry: bucket={request.bucket} cluster={request.cluster}"
        )
        try:
            self.db.delete_bucket(request.bucket, request.cluster)
            return ubdb_pb2.DeleteBucketEntryResponse()
        except Exception as e:
            self.set_context_error(context, e)
            return ubdb_pb2.DeleteBucketEntryResponse()

    def UpdateBucketEntry(self, request, context):
        logging.info(
            f"received: UpdateBucketEntry: bucket={request.bucket} cluster={request.cluster} state={request.state}"
        )
        if request.state == ubdb_pb2.BucketState.BUCKET_STATE_CREATED:
            bstate = BucketState.CREATED
        elif request.state == ubdb_pb2.BucketState.BUCKET_STATE_DELETING:
            bstate = BucketState.DELETING
        else:
            raise Exception(f"Unknown update state '{request.state}'")
        try:
            self.db.update_bucket(request.bucket, request.cluster, bstate)
            return ubdb_pb2.UpdateBucketEntryResponse()
        except Exception as e:
            self.set_context_error(context, e)
            return ubdb_pb2.UpdateBucketEntryResponse()


def _load_credential_from_file(filepath):
    """https://github.com/grpc/grpc/blob/master/examples/python/auth/_credentials.py"""
    real_path = os.path.join(os.path.dirname(__file__), filepath)
    with open(real_path, "rb") as f:
        return f.read()


def run(args):
    server_address = f"{args.address}:{args.port}"
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
            ca_crt = _load_credential_from_file(args.ca_cert)
            server_credentials = grpc.ssl_server_credentials(
                (
                    (
                        server_key,
                        server_crt,
                    ),
                ),
                (ca_crt),
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
    p.add_argument("address", type=str, help="Listen address", nargs="?", default="127.0.0.1")
    p.add_argument("port", type=int, help="Listen port", nargs="?", default=9000)
    p.add_argument(
        "-t", "--tls", help="connect to the server using TLS", action="store_true"
    )
    p.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    ptls = p.add_argument_group("TLS arguments")
    ptls.add_argument("--ca-cert", help="CA certificate file")
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
