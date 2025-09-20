import { useState, useEffect } from 'react'
import {
  Card,
  Table,
  Button,
  Modal,
  Form,
  Input,
  Select,
  Switch,
  message,
  Space,
  Tag
} from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'

interface AIModel {
  id: string
  name: string
  provider: string
  model_name: string
  base_url?: string
  api_key?: string
  enabled: boolean
  config: any
  created_at: string
}

const ModelManagement = () => {
  const [models, setModels] = useState<AIModel[]>([])
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingModel, setEditingModel] = useState<AIModel | null>(null)
  const [form] = Form.useForm()

  useEffect(() => {
    fetchModels()
  }, [])

  const fetchModels = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8001/api/models/')
      const data = await response.json()
      setModels(data)
    } catch (error) {
      message.error('获取模型列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = () => {
    setEditingModel(null)
    form.resetFields()
    setModalVisible(true)
  }

  const handleEdit = (model: AIModel) => {
    setEditingModel(model)
    form.setFieldsValue({
      ...model,
      api_key: model.api_key ? '********' : ''
    })
    setModalVisible(true)
  }

  const handleDelete = async (id: string) => {
    try {
      const response = await fetch(`http://localhost:8001/api/models/${id}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        message.success('模型删除成功')
        fetchModels()
      } else {
        message.error('模型删除失败')
      }
    } catch (error) {
      message.error('模型删除失败')
    }
  }

  const handleSubmit = async (values: any) => {
    try {
      const url = editingModel
        ? `http://localhost:8001/api/models/${editingModel.id}`
        : 'http://localhost:8001/api/models/'

      const method = editingModel ? 'PATCH' : 'POST'

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(values),
      })

      if (response.ok) {
        message.success(editingModel ? '模型更新成功' : '模型创建成功')
        setModalVisible(false)
        fetchModels()
      } else {
        message.error('操作失败')
      }
    } catch (error) {
      message.error('操作失败')
    }
  }

  const columns = [
    {
      title: '模型名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '提供商',
      dataIndex: 'provider',
      key: 'provider',
      render: (provider: string) => <Tag color="blue">{provider}</Tag>,
    },
    {
      title: '模型',
      dataIndex: 'model_name',
      key: 'model_name',
    },
    {
      title: '状态',
      dataIndex: 'enabled',
      key: 'enabled',
      render: (enabled: boolean) => (
        <Tag color={enabled ? 'green' : 'red'}>
          {enabled ? '启用' : '禁用'}
        </Tag>
      ),
    },
    {
      title: '操作',
      key: 'actions',
      render: (_: any, record: AIModel) => (
        <Space>
          <Button
            size="small"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Button
            size="small"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
          >
            删除
          </Button>
        </Space>
      ),
    },
  ]

  return (
    <div>
      <Card
        title="AI模型管理"
        bordered={false}
        extra={
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleCreate}
          >
            添加模型
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={models}
          loading={loading}
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={editingModel ? '编辑模型' : '添加模型'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            label="模型名称"
            name="name"
            rules={[{ required: true, message: '请输入模型名称' }]}
          >
            <Input placeholder="例如: GPT-4聊天模型" />
          </Form.Item>

          <Form.Item
            label="提供商"
            name="provider"
            rules={[{ required: true, message: '请选择提供商' }]}
          >
            <Select placeholder="选择模型提供商">
              <Select.Option value="openai">OpenAI</Select.Option>
              <Select.Option value="anthropic">Anthropic</Select.Option>
              <Select.Option value="ollama">Ollama</Select.Option>
              <Select.Option value="azure">Azure OpenAI</Select.Option>
              <Select.Option value="huggingface">Hugging Face</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="模型名称"
            name="model_name"
            rules={[{ required: true, message: '请输入模型名称' }]}
          >
            <Input placeholder="例如: gpt-4, claude-2, llama2" />
          </Form.Item>

          <Form.Item
            label="API地址"
            name="base_url"
          >
            <Input placeholder="对于本地模型如Ollama，请输入API地址" />
          </Form.Item>

          <Form.Item
            label="API密钥"
            name="api_key"
          >
            <Input.Password placeholder="输入API密钥（如需）" />
          </Form.Item>

          <Form.Item
            label="启用状态"
            name="enabled"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit">
              {editingModel ? '更新' : '创建'}
            </Button>
            <Button style={{ marginLeft: 8 }} onClick={() => setModalVisible(false)}>
              取消
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default ModelManagement