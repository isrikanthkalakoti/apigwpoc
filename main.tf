provider "aws" {
  region = "us-east-1"
}


resource "aws_api_gateway_rest_api" "example" {
  name           = "example-api"
  description    = "Example API"
  body           = file("openapispec.yml")
  api_key_source = "HEADER"
}

resource "aws_api_gateway_deployment" "example" {
  rest_api_id = aws_api_gateway_rest_api.example.id
}


resource "aws_api_gateway_stage" "example" {
  rest_api_id   = aws_api_gateway_rest_api.example.id
  deployment_id = aws_api_gateway_deployment.example.id
  stage_name    = "example"

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.example.arn
    format          = local.log_format
  }

  #xray_tracing_enabled = true
}


locals {
  log_format = jsonencode({ "requestId" : "$context.requestId",
  "ip" : "$context.identity.sourceIp",
  "requestTime" : "$context.requestTime",
  "httpMethod" : "$context.httpMethod",
  "resourcePath" : "$context.resourcePath",
  "status" : "$context.status",
  "protocol" : "$context.protocol",
  "responseLength" : "$context.responseLength",
  "apiId" : "$context.apiId",
  "userAgent" : "$context.identity.userAgent",
  "resourceId" : "$context.resourceId",
  "integrationLatency" : "$context.integrationLatency",
  "extendedRequestId" : "$context.extendedRequestId",
  "totalLatency" : "$context.responseLatency",
  "targetUrl" : "$context.method.request.url",
  "proxyUrl" : "https://$context.domainName$context.path"
  })
}

#context.integration.request.url
#context.integration.requestUrl
#context.integration.url
#context.integration.request.uri
#context.integration.uri


# resource "aws_xray_sampling_rule" "example_api_gateway_sampling_rule" {
#   rule_name      = "ExampleAPIGatewaySamplingRule"
#   priority       = 100
#   version        = 1
#   reservoir_size = 1
#   fixed_rate     = 0.01
#   url_path       = "*"
#   host           = "*"
#   http_method    = "*"
#   service_type   = "AWS::ApiGateway::Stage"
#   service_name   = "*"
#   resource_arn   = "*"
# }























