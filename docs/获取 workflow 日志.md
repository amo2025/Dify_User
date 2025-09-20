# 获取 workflow 日志

> 倒序返回 workflow 日志。

## OpenAPI

````yaml zh-hans/openapi_workflow.json get /workflows/logs
paths:
  path: /workflows/logs
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
      path: {}
      query:
        keyword:
          schema:
            - type: string
              description: （可选）关键字。
        status:
          schema:
            - type: enum<string>
              enum:
                - succeeded
                - failed
                - stopped
                - running
              description: （可选）执行状态：succeeded, failed, stopped, running。
        page:
          schema:
            - type: integer
              description: （可选）当前页码, 默认1。
              default: 1
        limit:
          schema:
            - type: integer
              description: （可选）每页条数, 默认20。
              default: 20
      header: {}
      cookie: {}
    body: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              page:
                allOf:
                  - type: integer
                    description: 当前页码。
              limit:
                allOf:
                  - type: integer
                    description: 每页条数。
              total:
                allOf:
                  - type: integer
                    description: 总条数。
              has_more:
                allOf:
                  - type: boolean
                    description: 是否还有更多数据。
              data:
                allOf:
                  - type: array
                    items:
                      $ref: '#/components/schemas/WorkflowLogItemCn'
                    description: 当前页码的数据。
            description: Workflow 日志列表响应。
            refIdentifier: '#/components/schemas/WorkflowLogsResponseCn'
        examples:
          example:
            value:
              page: 123
              limit: 123
              total: 123
              has_more: true
              data:
                - id: 3c90c3cc-0d44-4b50-8888-8dd25736052a
                  workflow_run:
                    id: 3c90c3cc-0d44-4b50-8888-8dd25736052a
                    version: <string>
                    status: running
                    error: <string>
                    elapsed_time: 123
                    total_tokens: 123
                    total_steps: 123
                    created_at: 123
                    finished_at: 123
                  created_from: <string>
                  created_by_role: <string>
                  created_by_account: 3c90c3cc-0d44-4b50-8888-8dd25736052a
                  created_by_end_user:
                    id: 3c90c3cc-0d44-4b50-8888-8dd25736052a
                    type: <string>
                    is_anonymous: true
                    session_id: <string>
                  created_at: 123
        description: 成功获取 workflow 日志。
  deprecated: false
  type: path
components:
  schemas:
    WorkflowLogItemCn:
      type: object
      description: 单条 Workflow 日志。
      properties:
        id:
          type: string
          format: uuid
          description: 标识。
        workflow_run:
          $ref: '#/components/schemas/WorkflowRunSummaryCn'
          description: Workflow 执行日志。
        created_from:
          type: string
          description: 来源。
        created_by_role:
          type: string
          description: 角色。
        created_by_account:
          type: string
          format: uuid
          nullable: true
          description: （可选）帐号。
        created_by_end_user:
          $ref: '#/components/schemas/EndUserSummaryCn'
          description: 用户。
        created_at:
          type: integer
          format: int64
          description: 创建时间。
    WorkflowRunSummaryCn:
      type: object
      description: Workflow 执行摘要信息。
      properties:
        id:
          type: string
          format: uuid
          description: 标识。
        version:
          type: string
          description: 版本。
        status:
          type: string
          enum:
            - running
            - succeeded
            - failed
            - stopped
          description: 执行状态。
        error:
          type: string
          nullable: true
          description: （可选）错误。
        elapsed_time:
          type: number
          format: float
          description: 耗时，单位秒。
        total_tokens:
          type: integer
          description: 消耗的token数量。
        total_steps:
          type: integer
          description: 执行步骤长度。
        created_at:
          type: integer
          format: int64
          description: 开始时间。
        finished_at:
          type: integer
          format: int64
          nullable: true
          description: 结束时间。
    EndUserSummaryCn:
      type: object
      description: 终端用户信息摘要。
      properties:
        id:
          type: string
          format: uuid
          description: 标识。
        type:
          type: string
          description: 类型。
        is_anonymous:
          type: boolean
          description: 是否匿名。
        session_id:
          type: string
          description: 会话标识。

````
