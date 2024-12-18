
resource "aws_cloudwatch_log_group" "example" {
  name              = "example-api-gateway-logs"
  retention_in_days = 30
}


