# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: services.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import types_pb2 as types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='services.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0eservices.proto\x1a\x0btypes.proto2\xc4\x06\n\nBLSSigning\x12\x61\n\x12GenerateKeypairRaw\x12$.bls_proto.GenerateKeypairRequestRaw\x1a%.bls_proto.GenerateKeypairResponseRaw\x12\x61\n\x12GenerateKeypairHex\x12$.bls_proto.GenerateKeypairRequestHex\x1a%.bls_proto.GenerateKeypairResponseHex\x12@\n\x07SignRaw\x12\x19.bls_proto.SignRequestRaw\x1a\x1a.bls_proto.SignResponseRaw\x12@\n\x07SignHex\x12\x19.bls_proto.SignRequestHex\x1a\x1a.bls_proto.SignResponseHex\x12\x43\n\tVerifyRaw\x12\x1b.bls_proto.VerifyRequestRaw\x1a\x19.bls_proto.VerifyResponse\x12\x43\n\tVerifyHex\x12\x1b.bls_proto.VerifyRequestHex\x1a\x19.bls_proto.VerifyResponse\x12O\n\x0c\x41ggregateRaw\x12\x1e.bls_proto.AggregateRequestRaw\x1a\x1f.bls_proto.AggregateResponseRaw\x12O\n\x0c\x41ggregateHex\x12\x1e.bls_proto.AggregateRequestHex\x1a\x1f.bls_proto.AggregateResponseHex\x12_\n\x13VerifyAggregatedRaw\x12$.bls_proto.VerifyAggregateRequestRaw\x1a\".bls_proto.VerifyAggregateResponse\x12_\n\x13VerifyAggregatedHex\x12$.bls_proto.VerifyAggregateRequestHex\x1a\".bls_proto.VerifyAggregateResponseb\x06proto3'
  ,
  dependencies=[types__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_BLSSIGNING = _descriptor.ServiceDescriptor(
  name='BLSSigning',
  full_name='BLSSigning',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=32,
  serialized_end=868,
  methods=[
  _descriptor.MethodDescriptor(
    name='GenerateKeypairRaw',
    full_name='BLSSigning.GenerateKeypairRaw',
    index=0,
    containing_service=None,
    input_type=types__pb2._GENERATEKEYPAIRREQUESTRAW,
    output_type=types__pb2._GENERATEKEYPAIRRESPONSERAW,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GenerateKeypairHex',
    full_name='BLSSigning.GenerateKeypairHex',
    index=1,
    containing_service=None,
    input_type=types__pb2._GENERATEKEYPAIRREQUESTHEX,
    output_type=types__pb2._GENERATEKEYPAIRRESPONSEHEX,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SignRaw',
    full_name='BLSSigning.SignRaw',
    index=2,
    containing_service=None,
    input_type=types__pb2._SIGNREQUESTRAW,
    output_type=types__pb2._SIGNRESPONSERAW,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SignHex',
    full_name='BLSSigning.SignHex',
    index=3,
    containing_service=None,
    input_type=types__pb2._SIGNREQUESTHEX,
    output_type=types__pb2._SIGNRESPONSEHEX,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='VerifyRaw',
    full_name='BLSSigning.VerifyRaw',
    index=4,
    containing_service=None,
    input_type=types__pb2._VERIFYREQUESTRAW,
    output_type=types__pb2._VERIFYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='VerifyHex',
    full_name='BLSSigning.VerifyHex',
    index=5,
    containing_service=None,
    input_type=types__pb2._VERIFYREQUESTHEX,
    output_type=types__pb2._VERIFYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='AggregateRaw',
    full_name='BLSSigning.AggregateRaw',
    index=6,
    containing_service=None,
    input_type=types__pb2._AGGREGATEREQUESTRAW,
    output_type=types__pb2._AGGREGATERESPONSERAW,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='AggregateHex',
    full_name='BLSSigning.AggregateHex',
    index=7,
    containing_service=None,
    input_type=types__pb2._AGGREGATEREQUESTHEX,
    output_type=types__pb2._AGGREGATERESPONSEHEX,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='VerifyAggregatedRaw',
    full_name='BLSSigning.VerifyAggregatedRaw',
    index=8,
    containing_service=None,
    input_type=types__pb2._VERIFYAGGREGATEREQUESTRAW,
    output_type=types__pb2._VERIFYAGGREGATERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='VerifyAggregatedHex',
    full_name='BLSSigning.VerifyAggregatedHex',
    index=9,
    containing_service=None,
    input_type=types__pb2._VERIFYAGGREGATEREQUESTHEX,
    output_type=types__pb2._VERIFYAGGREGATERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_BLSSIGNING)

DESCRIPTOR.services_by_name['BLSSigning'] = _BLSSIGNING

# @@protoc_insertion_point(module_scope)