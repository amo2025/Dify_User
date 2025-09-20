# 停止响应 (Workflow Task)

> 停止 workflow 任务的生成。仅支持流式模式。

## OpenAPI

````yaml zh-hans/openapi_workflow.json post /workflows/tasks/{task_id}/stop
paths:
  path: /workflows/tasks/{task_id}/stop
  method: post
  servers:
    - url: '{api_base_url}'
      description: API 的基础 URL。请将 {api_base_url} 替换为您的应用提供的实际 API 基础 URL。
      variables:
        api_base_url:
          type: string
          description: 实际的 API 基础 URL
          default: https://api.dify.ai/v1
  request:
    security:
      - title: ApiKeyAuth
        parameters:
          query: {}
          header:
            Authorization:
              type: http
              scheme: bearer
              description: >-
                API-Key 鉴权。所有 API 请求都应在 Authorization HTTP Header 中包含您的
                API-Key，格式为：Bearer {API_KEY}。强烈建议开发者把 API-Key 放在后端存储，而非客户端，以免泄露。
          cookie: {}
    parameters:
      path:
        task_id:
          schema:
            - type: string
              required: true
              description: 任务 ID，可在流式返回 Chunk 中获取。
              format: uuid
      query: {}
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              user:
                allOf:
                  - type: string
                    description: 用户标识，必须和执行 workflow 接口传入的 user 保持一致。
            required: true
            requiredProperties:
              - user
        examples:
          example:
            value:
              user: <string>
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              result:
                allOf:
                  - type: string
                    example: success
        examples:
          example:
            value:
              result: success
        description: 操作成功。
  deprecated: false
  type: path
components:
  schemas: {}

````
