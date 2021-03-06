# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc
import sys
sys.path.append("../../proto")

from backtesting import backtesting_pb2 as backtesting_dot_backtesting__pb2
from copytrade import copytrade_pb2 as copytrade_dot_copytrade__pb2


class BacktestingSrvStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.BacktestingTrade = channel.unary_unary(
        '/backtesting.BacktestingSrv/BacktestingTrade',
        request_serializer=backtesting_dot_backtesting__pb2.BacktestingTradeRequest.SerializeToString,
        response_deserializer=backtesting_dot_backtesting__pb2.BacktestingTradeResponse.FromString,
        )
    self.BacktestingUser = channel.unary_unary(
        '/backtesting.BacktestingSrv/BacktestingUser',
        request_serializer=backtesting_dot_backtesting__pb2.BacktestingUserRequest.SerializeToString,
        response_deserializer=backtesting_dot_backtesting__pb2.BacktestingUserResponse.FromString,
        )
    self.BacktestingUserCSV = channel.unary_unary(
        '/backtesting.BacktestingSrv/BacktestingUserCSV',
        request_serializer=backtesting_dot_backtesting__pb2.BacktestingUserCSVRequest.SerializeToString,
        response_deserializer=copytrade_dot_copytrade__pb2.Empty.FromString,
        )


class BacktestingSrvServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def BacktestingTrade(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def BacktestingUser(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def BacktestingUserCSV(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_BacktestingSrvServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'BacktestingTrade': grpc.unary_unary_rpc_method_handler(
          servicer.BacktestingTrade,
          request_deserializer=backtesting_dot_backtesting__pb2.BacktestingTradeRequest.FromString,
          response_serializer=backtesting_dot_backtesting__pb2.BacktestingTradeResponse.SerializeToString,
      ),
      'BacktestingUser': grpc.unary_unary_rpc_method_handler(
          servicer.BacktestingUser,
          request_deserializer=backtesting_dot_backtesting__pb2.BacktestingUserRequest.FromString,
          response_serializer=backtesting_dot_backtesting__pb2.BacktestingUserResponse.SerializeToString,
      ),
      'BacktestingUserCSV': grpc.unary_unary_rpc_method_handler(
          servicer.BacktestingUserCSV,
          request_deserializer=backtesting_dot_backtesting__pb2.BacktestingUserCSVRequest.FromString,
          response_serializer=copytrade_dot_copytrade__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'backtesting.BacktestingSrv', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
