# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ubdb/v1/ubdb.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12ubdb/v1/ubdb.proto\x12\x07ubdb.v1\"_\n\x15\x41\x64\x64\x42ucketEntryRequest\x12\x16\n\x06\x62ucket\x18\x01 \x01(\tR\x06\x62ucket\x12\x14\n\x05owner\x18\x02 \x01(\tR\x05owner\x12\x18\n\x07\x63luster\x18\x03 \x01(\tR\x07\x63luster\"\x18\n\x16\x41\x64\x64\x42ucketEntryResponse\"\x8e\x01\n\x18UpdateBucketEntryRequest\x12\x16\n\x06\x62ucket\x18\x01 \x01(\tR\x06\x62ucket\x12\x18\n\x07\x63luster\x18\x02 \x01(\tR\x07\x63luster\x12*\n\x05state\x18\x03 \x01(\x0e\x32\x14.ubdb.v1.BucketStateR\x05state\x12\x14\n\x05owner\x18\x04 \x01(\tR\x05owner\"\x1b\n\x19UpdateBucketEntryResponse\"b\n\x18\x44\x65leteBucketEntryRequest\x12\x16\n\x06\x62ucket\x18\x01 \x01(\tR\x06\x62ucket\x12\x18\n\x07\x63luster\x18\x02 \x01(\tR\x07\x63luster\x12\x14\n\x05owner\x18\x03 \x01(\tR\x05owner\"\x1b\n\x19\x44\x65leteBucketEntryResponse\"\x12\n\x10ReconcileRequest\"\x13\n\x11ReconcileResponse*`\n\x0b\x42ucketState\x12\x1c\n\x18\x42UCKET_STATE_UNSPECIFIED\x10\x00\x12\x18\n\x14\x42UCKET_STATE_CREATED\x10\x01\x12\x19\n\x15\x42UCKET_STATE_DELETING\x10\x02\x32\xdc\x02\n\x0bUBDBService\x12Q\n\x0e\x41\x64\x64\x42ucketEntry\x12\x1e.ubdb.v1.AddBucketEntryRequest\x1a\x1f.ubdb.v1.AddBucketEntryResponse\x12Z\n\x11\x44\x65leteBucketEntry\x12!.ubdb.v1.DeleteBucketEntryRequest\x1a\".ubdb.v1.DeleteBucketEntryResponse\x12Z\n\x11UpdateBucketEntry\x12!.ubdb.v1.UpdateBucketEntryRequest\x1a\".ubdb.v1.UpdateBucketEntryResponse\x12\x42\n\tReconcile\x12\x19.ubdb.v1.ReconcileRequest\x1a\x1a.ubdb.v1.ReconcileResponseB\x89\x01\n\x0b\x63om.ubdb.v1B\tUbdbProtoP\x01Z2bits.linode.com/StorageTeam/ubns/gen/proto/ubdb/v1\xa2\x02\x03UXX\xaa\x02\x07Ubdb.V1\xca\x02\x07Ubdb\\V1\xe2\x02\x13Ubdb\\V1\\GPBMetadata\xea\x02\x08Ubdb::V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ubdb.v1.ubdb_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\013com.ubdb.v1B\tUbdbProtoP\001Z2bits.linode.com/StorageTeam/ubns/gen/proto/ubdb/v1\242\002\003UXX\252\002\007Ubdb.V1\312\002\007Ubdb\\V1\342\002\023Ubdb\\V1\\GPBMetadata\352\002\010Ubdb::V1'
  _globals['_BUCKETSTATE']._serialized_start=498
  _globals['_BUCKETSTATE']._serialized_end=594
  _globals['_ADDBUCKETENTRYREQUEST']._serialized_start=31
  _globals['_ADDBUCKETENTRYREQUEST']._serialized_end=126
  _globals['_ADDBUCKETENTRYRESPONSE']._serialized_start=128
  _globals['_ADDBUCKETENTRYRESPONSE']._serialized_end=152
  _globals['_UPDATEBUCKETENTRYREQUEST']._serialized_start=155
  _globals['_UPDATEBUCKETENTRYREQUEST']._serialized_end=297
  _globals['_UPDATEBUCKETENTRYRESPONSE']._serialized_start=299
  _globals['_UPDATEBUCKETENTRYRESPONSE']._serialized_end=326
  _globals['_DELETEBUCKETENTRYREQUEST']._serialized_start=328
  _globals['_DELETEBUCKETENTRYREQUEST']._serialized_end=426
  _globals['_DELETEBUCKETENTRYRESPONSE']._serialized_start=428
  _globals['_DELETEBUCKETENTRYRESPONSE']._serialized_end=455
  _globals['_RECONCILEREQUEST']._serialized_start=457
  _globals['_RECONCILEREQUEST']._serialized_end=475
  _globals['_RECONCILERESPONSE']._serialized_start=477
  _globals['_RECONCILERESPONSE']._serialized_end=496
  _globals['_UBDBSERVICE']._serialized_start=597
  _globals['_UBDBSERVICE']._serialized_end=945
# @@protoc_insertion_point(module_scope)
