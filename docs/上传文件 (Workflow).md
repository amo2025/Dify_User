# 上传文件 (Workflow)

> 上传文件并在执行 workflow 时使用。支持您的工作流程所支持的任何格式。上传的文件仅供当前终端用户使用。

## OpenAPI

````yaml zh-hans/openapi_workflow.json post /files/upload
paths:
  path: /files/upload
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
      path: {}
      query: {}
      header: {}
      cookie: {}
    body:
      multipart/form-data:
        schemaArray:
          - type: object
            properties:
              file:
                allOf:
                  - type: string
                    format: binary
                    description: 要上传的文件。
              user:
                allOf:
                  - type: string
                    description: 用户标识。
            required: true
            requiredProperties:
              - file
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
              id:
                allOf:
                  - &ref_0
                    type: string
                    format: uuid
                    description: ID。
              name:
                allOf:
                  - &ref_1
                    type: string
                    description: 文件名。
              size:
                allOf:
                  - &ref_2
                    type: integer
                    description: 文件大小 (byte)。
              extension:
                allOf:
                  - &ref_3
                    type: string
                    description: 文件后缀。
              mime_type:
                allOf:
                  - &ref_4
                    type: string
                    description: 文件 mime-type。
              created_by:
                allOf:
                  - &ref_5
                    type: string
                    format: uuid
                    description: 上传人 ID (应为 uuid，示例中为 int，已修正)。
              created_at:
                allOf:
                  - &ref_6
                    type: integer
                    format: int64
                    description: 上传时间。
            description: 文件上传成功响应。
            refIdentifier: '#/components/schemas/FileUploadResponseCn'
        examples:
          example:
            value:
              id: 3c90c3cc-0d44-4b50-8888-8dd25736052a
              name: <string>
              size: 123
              extension: <string>
              mime_type: <string>
              created_by: 3c90c3cc-0d44-4b50-8888-8dd25736052a
              created_at: 123
        description: 文件上传成功。
    '201':
      application/json:
        schemaArray:
          - type: object
            properties:
              id:
                allOf:
                  - *ref_0
              name:
                allOf:
                  - *ref_1
              size:
                allOf:
                  - *ref_2
              extension:
                allOf:
                  - *ref_3
              mime_type:
                allOf:
                  - *ref_4
              created_by:
                allOf:
                  - *ref_5
              created_at:
                allOf:
                  - *ref_6
            description: 文件上传成功响应。
            refIdentifier: '#/components/schemas/FileUploadResponseCn'
        examples:
          example:
            value:
              id: 3c90c3cc-0d44-4b50-8888-8dd25736052a
              name: <string>
              size: 123
              extension: <string>
              mime_type: <string>
              created_by: 3c90c3cc-0d44-4b50-8888-8dd25736052a
              created_at: 123
        description: 文件创建成功。
    '400':
      application/json:
        schemaArray:
          - type: object
            properties:
              status:
                allOf:
                  - &ref_7
                    type: integer
                    nullable: true
                    description: HTTP 状态码。
              code:
                allOf:
                  - &ref_8
                    type: string
                    nullable: true
                    description: 错误码。
              message:
                allOf:
                  - &ref_9
                    type: string
                    description: 错误消息。
            description: 错误响应。
            refIdentifier: '#/components/schemas/ErrorResponseCn'
        examples:
          example:
            value:
              status: 123
              code: <string>
              message: <string>
        description: >-
          文件操作请求错误。可能错误码：no_file_uploaded, too_many_files, unsupported_preview,
          unsupported_estimate。
    '413':
      application/json:
        schemaArray:
          - type: object
            properties:
              status:
                allOf:
                  - *ref_7
              code:
                allOf:
                  - *ref_8
              message:
                allOf:
                  - *ref_9
            description: 错误响应。
            refIdentifier: '#/components/schemas/ErrorResponseCn'
        examples:
          example:
            value:
              status: 123
              code: <string>
              message: <string>
        description: 文件太大 (file_too_large)。
    '415':
      application/json:
        schemaArray:
          - type: object
            properties:
              status:
                allOf:
                  - *ref_7
              code:
                allOf:
                  - *ref_8
              message:
                allOf:
                  - *ref_9
            description: 错误响应。
            refIdentifier: '#/components/schemas/ErrorResponseCn'
        examples:
          example:
            value:
              status: 123
              code: <string>
              message: <string>
        description: 不支持的文件类型 (unsupported_file_type)。
    '500':
      application/json:
        schemaArray:
          - type: object
            properties:
              status:
                allOf:
                  - *ref_7
              code:
                allOf:
                  - *ref_8
              message:
                allOf:
                  - *ref_9
            description: 错误响应。
            refIdentifier: '#/components/schemas/ErrorResponseCn'
        examples:
          example:
            value:
              status: 123
              code: <string>
              message: <string>
        description: 服务内部异常。
    '503':
      application/json:
        schemaArray:
          - type: object
            properties:
              status:
                allOf:
                  - *ref_7
              code:
                allOf:
                  - *ref_8
              message:
                allOf:
                  - *ref_9
            description: 错误响应。
            refIdentifier: '#/components/schemas/ErrorResponseCn'
        examples:
          example:
            value:
              status: 123
              code: <string>
              message: <string>
        description: >-
          S3 存储服务错误。可能错误码：s3_connection_failed, s3_permission_denied,
          s3_file_too_large。
  deprecated: false
  type: path
components:
  schemas: {}

````
