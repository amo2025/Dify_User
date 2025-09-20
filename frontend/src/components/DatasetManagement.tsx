import { useState, useEffect } from 'react'
import { Card, Table, Button, message, Alert, Space, Tag, Modal, Upload } from 'antd'
import { PlusOutlined, FileOutlined, DeleteOutlined, UploadOutlined } from '@ant-design/icons'
import type { UploadFile, UploadProps } from 'antd'

interface Dataset {
  id: string
  name: string
  description: string
  document_count: number
  created_at: string
}

const DatasetManagement = () => {
  const [datasets, setDatasets] = useState<Dataset[]>([])
  const [loading, setLoading] = useState(false)
  const [uploadModalVisible, setUploadModalVisible] = useState(false)
  const [currentDatasetId, setCurrentDatasetId] = useState<string>('')
  const [fileList, setFileList] = useState<UploadFile[]>([])
  const [uploading, setUploading] = useState(false)

  useEffect(() => {
    fetchDatasets()
  }, [])

  const fetchDatasets = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8001/api/datasets/')
      if (response.ok) {
        const data = await response.json()
        setDatasets(data.data || [])
      } else {
        message.error('获取知识库列表失败')
      }
    } catch (error) {
      message.error('获取知识库列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateDataset = () => {
    message.info('创建知识库功能暂未实现')
  }

  const handleUploadFile = (datasetId: string) => {
    // 检查是否已配置Dify连接
    fetch('http://localhost:8001/api/config/')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        return response.json()
      })
      .then(config => {
        if (config.configured) {
          // 打开文件上传模态框
          setCurrentDatasetId(datasetId)
          setUploadModalVisible(true)
          setFileList([])
        } else {
          message.info('请先配置Dify连接信息')
        }
      })
      .catch(error => {
        console.error('配置检查失败:', error)
        message.info('请先配置Dify连接信息')
      })
  }

  const handleUpload = async (options: any) => {
    const { file, onSuccess, onError } = options

    setUploading(true)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('process_rule', 'automatic')
    formData.append('indexing_technique', 'high_quality')

    try {
      const response = await fetch(`http://localhost:8001/api/datasets/${currentDatasetId}/files`, {
        method: 'POST',
        body: formData
      })

      if (response.ok) {
        const result = await response.json()
        message.success('文件上传成功')
        onSuccess(result, file)
        setUploadModalVisible(false)
        fetchDatasets() // 刷新知识库列表
      } else {
        throw new Error('文件上传失败')
      }
    } catch (error) {
      message.error('文件上传失败')
      onError(error)
    } finally {
      setUploading(false)
    }
  }

  const uploadProps: UploadProps = {
    onRemove: (file) => {
      const index = fileList.indexOf(file)
      const newFileList = fileList.slice()
      newFileList.splice(index, 1)
      setFileList(newFileList)
    },
    beforeUpload: (file) => {
      setFileList([file])
      return false
    },
    fileList,
    showUploadList: true
  }

  const handleConfirmUpload = async () => {
    if (fileList.length === 0) {
      message.warning('请先选择文件')
      return
    }

    setUploading(true)

    const file = fileList[0]
    const formData = new FormData()
    formData.append('file', file as any)
    formData.append('process_rule', 'automatic')
    formData.append('indexing_technique', 'high_quality')

    try {
      const response = await fetch(`http://localhost:8001/api/datasets/${currentDatasetId}/files`, {
        method: 'POST',
        body: formData
      })

      if (response.ok) {
        const result = await response.json()
        message.success('文件上传成功')
        setUploadModalVisible(false)
        setFileList([])
        fetchDatasets() // 刷新知识库列表
      } else {
        const errorText = await response.text()
        throw new Error(errorText || '文件上传失败')
      }
    } catch (error) {
      console.error('上传失败:', error)
      message.error('文件上传失败')
    } finally {
      setUploading(false)
    }
  }

  const handleDeleteDataset = async (datasetId: string) => {
    try {
      const response = await fetch(`http://localhost:8001/api/datasets/${datasetId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        message.success('知识库删除成功')
        fetchDatasets()
      } else {
        message.error('知识库删除失败')
      }
    } catch (error) {
      message.error('知识库删除失败')
    }
  }

  const columns = [
    {
      title: '知识库名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: '文档数量',
      dataIndex: 'document_count',
      key: 'document_count',
      render: (count: number) => <Tag>{count} 个文档</Tag>,
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleDateString(),
    },
    {
      title: '操作',
      key: 'actions',
      render: (_: any, record: Dataset) => (
        <Space>
          <Button
            size="small"
            icon={<FileOutlined />}
            onClick={() => handleUploadFile(record.id)}
          >
            上传文件
          </Button>
          <Button
            size="small"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDeleteDataset(record.id)}
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
        title="知识库管理"
        bordered={false}
        extra={
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleCreateDataset}
          >
            创建知识库
          </Button>
        }
      >
        <Alert
          message="知识库功能说明"
          description="知识库管理功能依赖于Dify平台。请先完成Dify配置，然后您可以在这里管理知识库和文档。"
          type="info"
          showIcon
          style={{ marginBottom: 16 }}
        />

        <Table
          columns={columns}
          dataSource={datasets}
          loading={loading}
          rowKey="id"
          pagination={{ pageSize: 10 }}
          locale={{ emptyText: '暂无知识库数据' }}
        />
      </Card>

      <Modal
        title={`上传文件到知识库`}
        open={uploadModalVisible}
        onCancel={() => {
          setUploadModalVisible(false)
          setFileList([])
        }}
        footer={[
          <Button key="cancel" onClick={() => {
            setUploadModalVisible(false)
            setFileList([])
          }}>
            取消
          </Button>,
          <Button
            key="upload"
            type="primary"
            loading={uploading}
            onClick={handleConfirmUpload}
            disabled={fileList.length === 0}
          >
            {uploading ? '上传中...' : '确认上传'}
          </Button>
        ]}
        width={600}
      >
        <Upload.Dragger
          {...uploadProps}
          multiple={false}
          maxCount={1}
          accept=".txt,.pdf,.doc,.docx,.md,.html"
        >
          <p className="ant-upload-drag-icon">
            <UploadOutlined />
          </p>
          <p className="ant-upload-text">点击或拖拽文件到此处上传</p>
          <p className="ant-upload-hint">
            支持格式: TXT, PDF, DOC, DOCX, MD, HTML
          </p>
        </Upload.Dragger>

        {fileList.length > 0 && (
          <div style={{ marginTop: 16, padding: '8px 16px', background: '#f5f5f5', borderRadius: 4 }}>
            <strong>已选择文件:</strong> {fileList[0].name}
          </div>
        )}
      </Modal>
    </div>
  )
}

export default DatasetManagement