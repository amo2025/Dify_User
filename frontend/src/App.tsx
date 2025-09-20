import { useState } from 'react'
import { ConfigProvider, Layout, Menu, Typography, Grid, theme, Switch } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import {
  SettingOutlined,
  ApiOutlined,
  CodeOutlined,
  DatabaseOutlined,
  MenuOutlined,
  MoonOutlined,
  SunOutlined
} from '@ant-design/icons'

import ConfigManagement from './components/ConfigManagement'
import ModelManagement from './components/ModelManagement'
import WorkflowManagement from './components/WorkflowManagement'
import DatasetManagement from './components/DatasetManagement'

const { Header, Content, Sider } = Layout
const { Title } = Typography
const { useBreakpoint } = Grid

function App() {
  const [collapsed, setCollapsed] = useState(false)
  const [selectedKey, setSelectedKey] = useState('1')
  const [mobileMenuVisible, setMobileMenuVisible] = useState(false)
  const [darkMode, setDarkMode] = useState(false)
  const screens = useBreakpoint()

  // 移动端自动折叠菜单
  const isMobile = !screens.md
  const shouldCollapse = collapsed || isMobile

  const currentTheme = {
    algorithm: darkMode ? theme.darkAlgorithm : theme.defaultAlgorithm,
    token: {
      colorPrimary: '#1890ff',
      borderRadius: 8,
    },
  }

  return (
    <ConfigProvider locale={zhCN} theme={currentTheme}>
      <Layout style={{ minHeight: '100vh' }}>
        {/* 顶部导航栏 */}
        <Header style={{
          padding: isMobile ? '0 16px' : '0 24px',
          background: darkMode ? '#1f1f1f' : '#001529',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          boxShadow: darkMode ? '0 1px 4px rgba(255, 255, 255, 0.1)' : '0 1px 4px rgba(0, 0, 0, 0.1)',
          width: '100%',
          height: 64,
          lineHeight: '64px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            {isMobile && (
              <MenuOutlined
                onClick={() => setMobileMenuVisible(true)}
                style={{ fontSize: '18px', cursor: 'pointer' }}
              />
            )}
            <Title level={3} style={{ margin: 0, fontSize: isMobile ? '18px' : '20px', color: '#fff' }}>
              Dify Studio
            </Title>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            {!isMobile && (
              <span style={{ color: '#fff', fontSize: '14px' }}>
                本地Dify管理门户
              </span>
            )}
            <Switch
              checked={darkMode}
              onChange={setDarkMode}
              checkedChildren={<MoonOutlined />}
              unCheckedChildren={<SunOutlined />}
              style={{ marginLeft: '16px' }}
            />
          </div>
        </Header>

        <Layout>
          {/* 左侧菜单栏 */}
          {!isMobile && (
            <Sider
              collapsible
              collapsed={shouldCollapse}
              onCollapse={setCollapsed}
              theme="light"
              width={250}
              style={{
                background: darkMode ? '#1f1f1f' : '#fff',
                height: 'calc(100vh - 64px)',
                position: 'fixed',
                left: 0,
                top: 64,
                bottom: 0,
              }}
            >
              <Menu
                theme={darkMode ? "dark" : "light"}
                selectedKeys={[selectedKey]}
                mode="inline"
                items={[
                  {
                    key: '1',
                    icon: <SettingOutlined />,
                    label: '配置管理',
                  },
                  {
                    key: '2',
                    icon: <ApiOutlined />,
                    label: '模型管理',
                  },
                  {
                    key: '3',
                    icon: <CodeOutlined />,
                    label: '工作流管理',
                  },
                  {
                    key: '4',
                    icon: <DatabaseOutlined />,
                    label: '知识库管理',
                  },
                ]}
                onClick={({ key }) => setSelectedKey(key)}
                style={{
                  borderRight: 0,
                  marginTop: '16px'
                }}
              />
            </Sider>
          )}

          {/* 右侧内容区域 */}
          <Layout style={{
            marginLeft: !isMobile && !shouldCollapse ? 250 : !isMobile && shouldCollapse ? 80 : 0,
            background: 'transparent'
          }}>
            <Content style={{
              margin: isMobile ? '16px 8px' : '24px 16px',
              padding: isMobile ? '16px' : '24px',
              background: darkMode ? '#141414' : '#fff',
              borderRadius: 8,
              overflow: 'auto',
              minHeight: 'calc(100vh - 120px)'
            }}>
              {selectedKey === '1' && <ConfigManagement />}
              {selectedKey === '2' && <ModelManagement />}
              {selectedKey === '3' && <WorkflowManagement />}
              {selectedKey === '4' && <DatasetManagement />}
            </Content>
          </Layout>
        </Layout>
      </Layout>
    </ConfigProvider>
  )
}

export default App