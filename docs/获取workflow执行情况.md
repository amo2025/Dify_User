# 获取workflow执行情况

> 根据 workflow 执行 ID 获取 workflow 任务当前执行结果。

## OpenAPI

````yaml zh-hans/openapi_workflow.json get /workflows/run/{workflow_run_id}
paths:
  path: /workflows/run/{workflow_run_id}
  method: get
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
        workflow_run_id:
          schema:
            - type: string
              required: true
              description: workflow 执行 ID，可在流式返回 Chunk 或阻塞模式响应中获取。
              format: uuid
      query: {}
      header: {}
      cookie: {}
    body: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              id:
                allOf:
                  - type: string
                    format: uuid
                    description: workflow 执行 ID。
              workflow_id:
                allOf:
                  - type: string
                    format: uuid
                    description: 关联的 Workflow ID。
              status:
                allOf:
                  - type: string
                    enum:
                      - running
                      - succeeded
                      - failed
                      - stopped
                    description: 执行状态。
              inputs:
                allOf:
                  - type: string
                    description: 任务输入内容的 JSON 字符串。
              outputs:
                allOf:
                  - type: object
                    additionalProperties: true
                    nullable: true
                    description: 任务输出内容的 JSON 对象。
              error:
                allOf:
                  - type: string
                    nullable: true
                    description: 错误原因。
              total_steps:
                allOf:
                  - type: integer
                    description: 任务执行总步数。
              total_tokens:
                allOf:
                  - type: integer
                    description: 任务执行总 tokens。
              created_at:
                allOf:
                  - type: integer
                    format: int64
                    description: 任务开始时间。
              finished_at:
                allOf:
                  - type: integer
                    format: int64
                    nullable: true
                    description: 任务结束时间。
              elapsed_time:
                allOf:
                  - type: number
                    format: float
                    nullable: true
                    description: 耗时(秒)。
            description: Workflow 执行详情。
            refIdentifier: '#/components/schemas/WorkflowRunDetailResponseCn'
        examples:
          example:
            value:
              id: 3c90c3cc-0d44-4b50-8888-8dd25736052a
              workflow_id: 3c90c3cc-0d44-4b50-8888-8dd25736052a
              status: running
              inputs: <string>
              outputs: {}
              error: <string>
              total_steps: 123
              total_tokens: 123
              created_at: 123
              finished_at: 123
              elapsed_time: 123
        description: 成功获取 workflow 执行详情。
    '404':
      _mintlify/placeholder:
        schemaArray:
          - type: any
            description: Workflow 执行记录未找到。
        examples: {}
        description: Workflow 执行记录未找到。
  deprecated: false
  type: path
components:
  schemas: {}

````
