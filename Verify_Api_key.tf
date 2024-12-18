resource "aws_api_gateway_api_key" "example" {
  name        = "example-api-key"
  description = "Example API Key"
  enabled     = true
}

resource "aws_api_gateway_usage_plan" "example" {
  name        = "example-usage-plan"
  description = "example Usage Plan"

  api_stages {
    api_id = aws_api_gateway_rest_api.example.id
    stage  = aws_api_gateway_stage.example.stage_name
  }
}

resource "aws_api_gateway_usage_plan_key" "example" {
  key_id        = aws_api_gateway_api_key.example.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.example.id
}
