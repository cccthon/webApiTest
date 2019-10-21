# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tradesignal/tradesignal.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tradesignal/tradesignal.proto',
  package='tradesignal',
  syntax='proto3',
  serialized_pb=_b('\n\x1dtradesignal/tradesignal.proto\x12\x0btradesignal\"\xe2\x03\n\x0bTradeSignal\x12$\n\x04Mode\x18\x01 \x01(\x0e\x32\x16.tradesignal.TradeMode\x12\x10\n\x08\x42rokerID\x18\x02 \x01(\x05\x12\x0f\n\x07\x41\x63\x63ount\x18\x03 \x01(\t\x12\x0f\n\x07TradeID\x18\x04 \x01(\x05\x12\x0e\n\x06Symbol\x18\x05 \x01(\t\x12\"\n\x03\x43md\x18\x06 \x01(\x0e\x32\x15.tradesignal.TradeCmd\x12\x10\n\x08Quantity\x18\x07 \x01(\x01\x12\x14\n\x0c\x43ontractSize\x18\x08 \x01(\x01\x12\x11\n\tOpenPrice\x18\t \x01(\x01\x12\x10\n\x08OpenTime\x18\n \x01(\x03\x12\x12\n\nClosePrice\x18\x0b \x01(\x01\x12\x11\n\tCloseTime\x18\x0c \x01(\x03\x12\x11\n\tToTradeID\x18\r \x01(\x05\x12\x0f\n\x07\x43omment\x18\x0e \x01(\t\x12\x0e\n\x06\x44igits\x18\x0f \x01(\x05\x12\r\n\x05Swaps\x18\x10 \x01(\x01\x12\x12\n\nCommission\x18\x11 \x01(\x01\x12\r\n\x05Taxes\x18\x12 \x01(\x01\x12\n\n\x02SL\x18\x13 \x01(\x01\x12\n\n\x02TP\x18\x14 \x01(\x01\x12\x0e\n\x06Profit\x18\x15 \x01(\x01\x12\x0f\n\x07OrderID\x18\x16 \x01(\x05\x12\x11\n\tSLOrderID\x18\x17 \x01(\x05\x12\x11\n\tTPOrderID\x18\x18 \x01(\x05\x12\x0c\n\x04Lots\x18\x19 \x01(\x01\"\x8c\x03\n\x0c\x41\x63\x63ountAsset\x12\n\n\x02ID\x18\x01 \x01(\x05\x12\x0e\n\x06UserID\x18\x02 \x01(\x05\x12\x0f\n\x07\x41\x63\x63ount\x18\x03 \x01(\t\x12\x10\n\x08\x42rokerID\x18\x04 \x01(\x05\x12\x0f\n\x07\x42\x61lance\x18\x05 \x01(\x01\x12\x0e\n\x06Profit\x18\x06 \x01(\x01\x12\x0e\n\x06\x43redit\x18\x07 \x01(\x01\x12\x0e\n\x06\x45quity\x18\x08 \x01(\x01\x12\x0e\n\x06Margin\x18\t \x01(\x01\x12\x13\n\x0bMarginLevel\x18\n \x01(\x01\x12\x12\n\nMarginFree\x18\x0b \x01(\x01\x12\r\n\x05Group\x18\x0c \x01(\t\x12\x0e\n\x06\x45nable\x18\r \x01(\x05\x12\x18\n\x10PrevMonthBalance\x18\x0e \x01(\x01\x12\x13\n\x0bPrevBalance\x18\x0f \x01(\x01\x12\x14\n\x0cInterestrate\x18\x10 \x01(\x01\x12\x16\n\x0eManagerAccount\x18\x11 \x01(\t\x12\x0f\n\x07RegDate\x18\x12 \x01(\x03\x12\x10\n\x08LastDate\x18\x13 \x01(\x03\x12\x12\n\nModifyTime\x18\x14 \x01(\x03\x12\x10\n\x08Leverage\x18\x15 \x01(\x05\"u\n\x16TradeSignalListRequest\x12\x0f\n\x07\x41\x63\x63ount\x18\x01 \x01(\t\x12\x0c\n\x04\x46rom\x18\x02 \x01(\x03\x12\n\n\x02To\x18\x03 \x01(\x03\x12\x15\n\rLimitPosition\x18\x04 \x01(\x08\x12\x19\n\x11LimitPendingOrder\x18\x05 \x01(\x08\"M\n\x14TradeSignalListReply\x12&\n\x04List\x18\x01 \x03(\x0b\x32\x18.tradesignal.TradeSignal\x12\r\n\x05\x43ount\x18\x02 \x01(\x05\"y\n\x14SubscribeTradeSignal\x12&\n\x04List\x18\x01 \x03(\x0b\x32\x18.tradesignal.TradeSignal\x12\r\n\x05\x43ount\x18\x02 \x01(\x05\x12*\n\x04Type\x18\x03 \x01(\x0e\x32\x1c.tradesignal.TradeSignalType*,\n\tTradeMode\x12\x07\n\x03\x41\x64\x64\x10\x00\x12\n\n\x06Update\x10\x01\x12\n\n\x06\x44\x65lete\x10\x02*n\n\x08TradeCmd\x12\x07\n\x03\x42uy\x10\x00\x12\x08\n\x04Sell\x10\x01\x12\x0c\n\x08\x42uyLimit\x10\x02\x12\r\n\tSellLimit\x10\x03\x12\x0b\n\x07\x42uyStop\x10\x04\x12\x0c\n\x08SellStop\x10\x05\x12\x0b\n\x07\x42\x61lance\x10\x06\x12\n\n\x06\x43redit\x10\x07*R\n\x0fTradeSignalType\x12\x13\n\x0fTradeSignalInit\x10\x00\x12\x13\n\x0fTradeSignalSync\x10\x01\x12\x15\n\x11TradeSignalUpdate\x10\x02\x42 \xaa\x02\x1d\x43sharpGRPCLibrary.TradeSignalb\x06proto3')
)

_TRADEMODE = _descriptor.EnumDescriptor(
  name='TradeMode',
  full_name='tradesignal.TradeMode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Add', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Update', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Delete', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1251,
  serialized_end=1295,
)
_sym_db.RegisterEnumDescriptor(_TRADEMODE)

TradeMode = enum_type_wrapper.EnumTypeWrapper(_TRADEMODE)
_TRADECMD = _descriptor.EnumDescriptor(
  name='TradeCmd',
  full_name='tradesignal.TradeCmd',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Buy', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Sell', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BuyLimit', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SellLimit', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BuyStop', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SellStop', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Balance', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Credit', index=7, number=7,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1297,
  serialized_end=1407,
)
_sym_db.RegisterEnumDescriptor(_TRADECMD)

TradeCmd = enum_type_wrapper.EnumTypeWrapper(_TRADECMD)
_TRADESIGNALTYPE = _descriptor.EnumDescriptor(
  name='TradeSignalType',
  full_name='tradesignal.TradeSignalType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TradeSignalInit', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TradeSignalSync', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TradeSignalUpdate', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1409,
  serialized_end=1491,
)
_sym_db.RegisterEnumDescriptor(_TRADESIGNALTYPE)

TradeSignalType = enum_type_wrapper.EnumTypeWrapper(_TRADESIGNALTYPE)
Add = 0
Update = 1
Delete = 2
Buy = 0
Sell = 1
BuyLimit = 2
SellLimit = 3
BuyStop = 4
SellStop = 5
Balance = 6
Credit = 7
TradeSignalInit = 0
TradeSignalSync = 1
TradeSignalUpdate = 2



_TRADESIGNAL = _descriptor.Descriptor(
  name='TradeSignal',
  full_name='tradesignal.TradeSignal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Mode', full_name='tradesignal.TradeSignal.Mode', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='BrokerID', full_name='tradesignal.TradeSignal.BrokerID', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Account', full_name='tradesignal.TradeSignal.Account', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='TradeID', full_name='tradesignal.TradeSignal.TradeID', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Symbol', full_name='tradesignal.TradeSignal.Symbol', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Cmd', full_name='tradesignal.TradeSignal.Cmd', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Quantity', full_name='tradesignal.TradeSignal.Quantity', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ContractSize', full_name='tradesignal.TradeSignal.ContractSize', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='OpenPrice', full_name='tradesignal.TradeSignal.OpenPrice', index=8,
      number=9, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='OpenTime', full_name='tradesignal.TradeSignal.OpenTime', index=9,
      number=10, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ClosePrice', full_name='tradesignal.TradeSignal.ClosePrice', index=10,
      number=11, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='CloseTime', full_name='tradesignal.TradeSignal.CloseTime', index=11,
      number=12, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ToTradeID', full_name='tradesignal.TradeSignal.ToTradeID', index=12,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Comment', full_name='tradesignal.TradeSignal.Comment', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Digits', full_name='tradesignal.TradeSignal.Digits', index=14,
      number=15, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Swaps', full_name='tradesignal.TradeSignal.Swaps', index=15,
      number=16, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Commission', full_name='tradesignal.TradeSignal.Commission', index=16,
      number=17, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Taxes', full_name='tradesignal.TradeSignal.Taxes', index=17,
      number=18, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='SL', full_name='tradesignal.TradeSignal.SL', index=18,
      number=19, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='TP', full_name='tradesignal.TradeSignal.TP', index=19,
      number=20, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Profit', full_name='tradesignal.TradeSignal.Profit', index=20,
      number=21, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='OrderID', full_name='tradesignal.TradeSignal.OrderID', index=21,
      number=22, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='SLOrderID', full_name='tradesignal.TradeSignal.SLOrderID', index=22,
      number=23, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='TPOrderID', full_name='tradesignal.TradeSignal.TPOrderID', index=23,
      number=24, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Lots', full_name='tradesignal.TradeSignal.Lots', index=24,
      number=25, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=47,
  serialized_end=529,
)


_ACCOUNTASSET = _descriptor.Descriptor(
  name='AccountAsset',
  full_name='tradesignal.AccountAsset',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ID', full_name='tradesignal.AccountAsset.ID', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='UserID', full_name='tradesignal.AccountAsset.UserID', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Account', full_name='tradesignal.AccountAsset.Account', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='BrokerID', full_name='tradesignal.AccountAsset.BrokerID', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Balance', full_name='tradesignal.AccountAsset.Balance', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Profit', full_name='tradesignal.AccountAsset.Profit', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Credit', full_name='tradesignal.AccountAsset.Credit', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Equity', full_name='tradesignal.AccountAsset.Equity', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Margin', full_name='tradesignal.AccountAsset.Margin', index=8,
      number=9, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='MarginLevel', full_name='tradesignal.AccountAsset.MarginLevel', index=9,
      number=10, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='MarginFree', full_name='tradesignal.AccountAsset.MarginFree', index=10,
      number=11, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Group', full_name='tradesignal.AccountAsset.Group', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Enable', full_name='tradesignal.AccountAsset.Enable', index=12,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='PrevMonthBalance', full_name='tradesignal.AccountAsset.PrevMonthBalance', index=13,
      number=14, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='PrevBalance', full_name='tradesignal.AccountAsset.PrevBalance', index=14,
      number=15, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Interestrate', full_name='tradesignal.AccountAsset.Interestrate', index=15,
      number=16, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ManagerAccount', full_name='tradesignal.AccountAsset.ManagerAccount', index=16,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='RegDate', full_name='tradesignal.AccountAsset.RegDate', index=17,
      number=18, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='LastDate', full_name='tradesignal.AccountAsset.LastDate', index=18,
      number=19, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ModifyTime', full_name='tradesignal.AccountAsset.ModifyTime', index=19,
      number=20, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Leverage', full_name='tradesignal.AccountAsset.Leverage', index=20,
      number=21, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=532,
  serialized_end=928,
)


_TRADESIGNALLISTREQUEST = _descriptor.Descriptor(
  name='TradeSignalListRequest',
  full_name='tradesignal.TradeSignalListRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Account', full_name='tradesignal.TradeSignalListRequest.Account', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='From', full_name='tradesignal.TradeSignalListRequest.From', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='To', full_name='tradesignal.TradeSignalListRequest.To', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='LimitPosition', full_name='tradesignal.TradeSignalListRequest.LimitPosition', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='LimitPendingOrder', full_name='tradesignal.TradeSignalListRequest.LimitPendingOrder', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=930,
  serialized_end=1047,
)


_TRADESIGNALLISTREPLY = _descriptor.Descriptor(
  name='TradeSignalListReply',
  full_name='tradesignal.TradeSignalListReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='List', full_name='tradesignal.TradeSignalListReply.List', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Count', full_name='tradesignal.TradeSignalListReply.Count', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1049,
  serialized_end=1126,
)


_SUBSCRIBETRADESIGNAL = _descriptor.Descriptor(
  name='SubscribeTradeSignal',
  full_name='tradesignal.SubscribeTradeSignal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='List', full_name='tradesignal.SubscribeTradeSignal.List', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Count', full_name='tradesignal.SubscribeTradeSignal.Count', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Type', full_name='tradesignal.SubscribeTradeSignal.Type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1128,
  serialized_end=1249,
)

_TRADESIGNAL.fields_by_name['Mode'].enum_type = _TRADEMODE
_TRADESIGNAL.fields_by_name['Cmd'].enum_type = _TRADECMD
_TRADESIGNALLISTREPLY.fields_by_name['List'].message_type = _TRADESIGNAL
_SUBSCRIBETRADESIGNAL.fields_by_name['List'].message_type = _TRADESIGNAL
_SUBSCRIBETRADESIGNAL.fields_by_name['Type'].enum_type = _TRADESIGNALTYPE
DESCRIPTOR.message_types_by_name['TradeSignal'] = _TRADESIGNAL
DESCRIPTOR.message_types_by_name['AccountAsset'] = _ACCOUNTASSET
DESCRIPTOR.message_types_by_name['TradeSignalListRequest'] = _TRADESIGNALLISTREQUEST
DESCRIPTOR.message_types_by_name['TradeSignalListReply'] = _TRADESIGNALLISTREPLY
DESCRIPTOR.message_types_by_name['SubscribeTradeSignal'] = _SUBSCRIBETRADESIGNAL
DESCRIPTOR.enum_types_by_name['TradeMode'] = _TRADEMODE
DESCRIPTOR.enum_types_by_name['TradeCmd'] = _TRADECMD
DESCRIPTOR.enum_types_by_name['TradeSignalType'] = _TRADESIGNALTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TradeSignal = _reflection.GeneratedProtocolMessageType('TradeSignal', (_message.Message,), dict(
  DESCRIPTOR = _TRADESIGNAL,
  __module__ = 'tradesignal.tradesignal_pb2'
  # @@protoc_insertion_point(class_scope:tradesignal.TradeSignal)
  ))
_sym_db.RegisterMessage(TradeSignal)

AccountAsset = _reflection.GeneratedProtocolMessageType('AccountAsset', (_message.Message,), dict(
  DESCRIPTOR = _ACCOUNTASSET,
  __module__ = 'tradesignal.tradesignal_pb2'
  # @@protoc_insertion_point(class_scope:tradesignal.AccountAsset)
  ))
_sym_db.RegisterMessage(AccountAsset)

TradeSignalListRequest = _reflection.GeneratedProtocolMessageType('TradeSignalListRequest', (_message.Message,), dict(
  DESCRIPTOR = _TRADESIGNALLISTREQUEST,
  __module__ = 'tradesignal.tradesignal_pb2'
  # @@protoc_insertion_point(class_scope:tradesignal.TradeSignalListRequest)
  ))
_sym_db.RegisterMessage(TradeSignalListRequest)

TradeSignalListReply = _reflection.GeneratedProtocolMessageType('TradeSignalListReply', (_message.Message,), dict(
  DESCRIPTOR = _TRADESIGNALLISTREPLY,
  __module__ = 'tradesignal.tradesignal_pb2'
  # @@protoc_insertion_point(class_scope:tradesignal.TradeSignalListReply)
  ))
_sym_db.RegisterMessage(TradeSignalListReply)

SubscribeTradeSignal = _reflection.GeneratedProtocolMessageType('SubscribeTradeSignal', (_message.Message,), dict(
  DESCRIPTOR = _SUBSCRIBETRADESIGNAL,
  __module__ = 'tradesignal.tradesignal_pb2'
  # @@protoc_insertion_point(class_scope:tradesignal.SubscribeTradeSignal)
  ))
_sym_db.RegisterMessage(SubscribeTradeSignal)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\252\002\035CsharpGRPCLibrary.TradeSignal'))
# @@protoc_insertion_point(module_scope)