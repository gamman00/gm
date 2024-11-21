// Generated by gencpp from file object_pallezting/SetTarget.msg
// DO NOT EDIT!


#ifndef OBJECT_PALLEZTING_MESSAGE_SETTARGET_H
#define OBJECT_PALLEZTING_MESSAGE_SETTARGET_H

#include <ros/service_traits.h>


#include <object_pallezting/SetTargetRequest.h>
#include <object_pallezting/SetTargetResponse.h>


namespace object_pallezting
{

struct SetTarget
{

typedef SetTargetRequest Request;
typedef SetTargetResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct SetTarget
} // namespace object_pallezting


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::object_pallezting::SetTarget > {
  static const char* value()
  {
    return "15a6bbca6b7bdaa8c9ab1c07de00a6ac";
  }

  static const char* value(const ::object_pallezting::SetTarget&) { return value(); }
};

template<>
struct DataType< ::object_pallezting::SetTarget > {
  static const char* value()
  {
    return "object_pallezting/SetTarget";
  }

  static const char* value(const ::object_pallezting::SetTarget&) { return value(); }
};


// service_traits::MD5Sum< ::object_pallezting::SetTargetRequest> should match
// service_traits::MD5Sum< ::object_pallezting::SetTarget >
template<>
struct MD5Sum< ::object_pallezting::SetTargetRequest>
{
  static const char* value()
  {
    return MD5Sum< ::object_pallezting::SetTarget >::value();
  }
  static const char* value(const ::object_pallezting::SetTargetRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::object_pallezting::SetTargetRequest> should match
// service_traits::DataType< ::object_pallezting::SetTarget >
template<>
struct DataType< ::object_pallezting::SetTargetRequest>
{
  static const char* value()
  {
    return DataType< ::object_pallezting::SetTarget >::value();
  }
  static const char* value(const ::object_pallezting::SetTargetRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::object_pallezting::SetTargetResponse> should match
// service_traits::MD5Sum< ::object_pallezting::SetTarget >
template<>
struct MD5Sum< ::object_pallezting::SetTargetResponse>
{
  static const char* value()
  {
    return MD5Sum< ::object_pallezting::SetTarget >::value();
  }
  static const char* value(const ::object_pallezting::SetTargetResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::object_pallezting::SetTargetResponse> should match
// service_traits::DataType< ::object_pallezting::SetTarget >
template<>
struct DataType< ::object_pallezting::SetTargetResponse>
{
  static const char* value()
  {
    return DataType< ::object_pallezting::SetTarget >::value();
  }
  static const char* value(const ::object_pallezting::SetTargetResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // OBJECT_PALLEZTING_MESSAGE_SETTARGET_H