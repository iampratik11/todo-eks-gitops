data "aws_caller_identity" "current" {}

data "aws_iam_openid_connect_provider" "eks" {
  url = "https://${module.eks.oidc_provider}"
}

resource "aws_iam_policy" "todo_backend_dynamodb" {
  name        = "todo-backend-dynamodb-policy"
  description = "Allow Todo backend to access its DynamoDB table"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan"
        ]

        Resource = "arn:aws:dynamodb:us-east-2:${data.aws_caller_identity.current.account_id}:table/todo-app-todos"
      }
    ]
  })
}

resource "aws_iam_role" "todo_backend" {
  name = "todo-backend-dynamodb-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Federated = data.aws_iam_openid_connect_provider.eks.arn
        }

        Action = "sts:AssumeRoleWithWebIdentity"

        Condition = {
          StringEquals = {
            "${replace(module.eks.oidc_provider, "https://", "")}:aud" = "sts.amazonaws.com"

            "${replace(module.eks.oidc_provider, "https://", "")}:sub" = "system:serviceaccount:default:todo-backend"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "todo_backend_dynamodb" {
  role       = aws_iam_role.todo_backend.name
  policy_arn = aws_iam_policy.todo_backend_dynamodb.arn
}

output "todo_backend_iam_role_arn" {
  value = aws_iam_role.todo_backend.arn
}
