import { useState } from 'react'
import { Card, Button, message, Alert } from 'antd'
import { PlayCircleOutlined } from '@ant-design/icons'

const WorkflowManagement = () => {
  const [loading, setLoading] = useState(false)

  const handleRunWorkflow = async () => {
    setLoading(true)
    try {
      // 这里需要实现工作流运行逻辑
      // 暂时显示提示信息
      message.info('工作流功能需要先配置Dify连接信息')
    } catch (error) {
      message.error('工作流执行失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Card title="工作流管理" bordered={false}>
        <Alert
          message="工作流功能说明"
          description="工作流管理功能依赖于Dify平台。请先完成Dify配置，然后您可以在这里运行和管理工作流。"
          type="info"
          showIcon
          style={{ marginBottom: 16 }}
        />

        <div style={{ textAlign: 'center', padding: '40px 0' }}>
          <Button
            type="primary"
            size="large"
            icon={<PlayCircleOutlined />}
            loading={loading}
            onClick={handleRunWorkflow}
          >
            运行工作流
          </Button>

          <div style={{ marginTop: 16, color: '#666' }}>
            <p>功能包括：</p>
            <ul style={{ textAlign: 'left', display: 'inline-block' }}>
              <li>工作流执行和监控</li>
              <li>执行历史查看</li>
              <li>智能DSL生成</li>
              <li>工作流调试</li>
            </ul>
          </div>
        </div>
      </Card>
    </div>
  )
}

export default WorkflowManagement