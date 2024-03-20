# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from ubdb.v1 import ubdb_pb2 as ubdb_dot_v1_dot_ubdb__pb2


class UBDBServiceStub(object):
    """UBDBService provides an endpoint for UBDB.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AddBucketEntry = channel.unary_unary(
                '/ubdb.v1.UBDBService/AddBucketEntry',
                request_serializer=ubdb_dot_v1_dot_ubdb__pb2.AddBucketEntryRequest.SerializeToString,
                response_deserializer=ubdb_dot_v1_dot_ubdb__pb2.AddBucketEntryResponse.FromString,
                )
        self.DeleteBucketEntry = channel.unary_unary(
                '/ubdb.v1.UBDBService/DeleteBucketEntry',
                request_serializer=ubdb_dot_v1_dot_ubdb__pb2.DeleteBucketEntryRequest.SerializeToString,
                response_deserializer=ubdb_dot_v1_dot_ubdb__pb2.DeleteBucketEntryResponse.FromString,
                )
        self.UpdateBucketEntry = channel.unary_unary(
                '/ubdb.v1.UBDBService/UpdateBucketEntry',
                request_serializer=ubdb_dot_v1_dot_ubdb__pb2.UpdateBucketEntryRequest.SerializeToString,
                response_deserializer=ubdb_dot_v1_dot_ubdb__pb2.UpdateBucketEntryResponse.FromString,
                )


class UBDBServiceServicer(object):
    """UBDBService provides an endpoint for UBDB.
    """

    def AddBucketEntry(self, request, context):
        """AddBucketEntry creates a new BucketEntry in UBDB.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteBucketEntry(self, request, context):
        """DeleteBucketEntry deletes a BucketEntry in UBDB.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateBucketEntry(self, request, context):
        """UpdateBucketEntry deletes a BucketEntry in UBDB.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UBDBServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AddBucketEntry': grpc.unary_unary_rpc_method_handler(
                    servicer.AddBucketEntry,
                    request_deserializer=ubdb_dot_v1_dot_ubdb__pb2.AddBucketEntryRequest.FromString,
                    response_serializer=ubdb_dot_v1_dot_ubdb__pb2.AddBucketEntryResponse.SerializeToString,
            ),
            'DeleteBucketEntry': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteBucketEntry,
                    request_deserializer=ubdb_dot_v1_dot_ubdb__pb2.DeleteBucketEntryRequest.FromString,
                    response_serializer=ubdb_dot_v1_dot_ubdb__pb2.DeleteBucketEntryResponse.SerializeToString,
            ),
            'UpdateBucketEntry': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateBucketEntry,
                    request_deserializer=ubdb_dot_v1_dot_ubdb__pb2.UpdateBucketEntryRequest.FromString,
                    response_serializer=ubdb_dot_v1_dot_ubdb__pb2.UpdateBucketEntryResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ubdb.v1.UBDBService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class UBDBService(object):
    """UBDBService provides an endpoint for UBDB.
    """

    @staticmethod
    def AddBucketEntry(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ubdb.v1.UBDBService/AddBucketEntry',
            ubdb_dot_v1_dot_ubdb__pb2.AddBucketEntryRequest.SerializeToString,
            ubdb_dot_v1_dot_ubdb__pb2.AddBucketEntryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteBucketEntry(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ubdb.v1.UBDBService/DeleteBucketEntry',
            ubdb_dot_v1_dot_ubdb__pb2.DeleteBucketEntryRequest.SerializeToString,
            ubdb_dot_v1_dot_ubdb__pb2.DeleteBucketEntryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateBucketEntry(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ubdb.v1.UBDBService/UpdateBucketEntry',
            ubdb_dot_v1_dot_ubdb__pb2.UpdateBucketEntryRequest.SerializeToString,
            ubdb_dot_v1_dot_ubdb__pb2.UpdateBucketEntryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
