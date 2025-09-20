import { useState, useEffect } from 'react'
import { Card, Form, Input, Button, message, Alert, Spin } from 'antd'
import { SettingOutlined, CheckCircleOutlined } from '@ant-design/icons'

interface Config {
  base_url: string
  api_key: string
  configured: boolean
}

const ConfigManagement = () => {
  const [form] = Form.useForm()
  const [config, setConfig] = useState<Config | null>(null)
  const [loading, setLoading] = useState(true)
  const [testing, setTesting] = useState(false)

  useEffect(() => {
    fetchConfig()
  }, [])

  const fetchConfig = async () => {
    try {
      const response = await fetch('/api/config/')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      setConfig(data)
      form.setFieldsValue({
        base_url: data.base_url,
        api_key: data.configured ? '********' : ''
      })
    } catch (error) {
      console.error('获取配置失败:', error)
      message.error('获取配置失败，请检查后端服务是否正常')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async (values: any) => {
    try {
      const response = await fetch('/api/config/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(values),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      message.success(result.message || '配置保存成功')
      fetchConfig()
    } catch (error: any) {
      console.error('配置保存失败:', error)
      message.error(`配置保存失败: ${error.message || '未知错误'}`)
    }
  }

  const testConnection = async () => {
    setTesting(true)
    try {
      const response = await fetch('/api/config/test')

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      message.success(data.message || '连接测试成功')
    } catch (error: any) {
      console.error('连接测试失败:', error)
      message.error(`连接测试失败: ${error.message || '未知错误'}`)
    } finally {
      setTesting(false)
    }
  }

  if (loading) {
    return <Spin size="large" />
  }

  return (
    <div>
      <Card title="Dify配置管理">
        {config && !config.configured && (
          <Alert
            message="请先配置Dify连接信息"
            description="需要配置Dify API地址和密钥才能使用完整功能"
            type="warning"
            showIcon
            style={{ marginBottom: 16 }}
          />
        )}

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSave}
          initialValues={{
            base_url: 'http://localhost:8091/',
            api_key: ''
          }}
        >
          <Form.Item
            label="Dify API地址"
            name="base_url"
            rules={[{ required: true, message: '请输入API地址' }]}
          >
            <Input placeholder="http://localhost:8091/" />
          </Form.Item>

          <Form.Item
            label="API密钥"
            name="api_key"
            rules={[{ required: true, message: '请输入API密钥' }]}
          >
            <Input.Password placeholder="输入您的Dify API密钥" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" icon={<SettingOutlined />}>
              保存配置
            </Button>
            <Button
              style={{ marginLeft: 8 }}
              onClick={testConnection}
              loading={testing}
              icon={<CheckCircleOutlined />}
              disabled={!config?.configured}
            >
              测试连接
            </Button>
          </Form.Item>
        </Form>

        {config?.configured && (
          <Alert
            message="配置已生效"
            description={`当前配置: ${config.base_url}`}
            type="success"
            showIcon
          />
        )}
      </Card>
    </div>
  )
}

export default ConfigManagement