import React, { useEffect, useState } from "react";
import {  Layout, theme } from "antd";
import { Outlet, useNavigate, useLocation } from "react-router-dom";

const {Content } = Layout;

const MyLayout: React.FC = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const items = [
    { key: "1", label: "Invoices", path: "/dashboard" },
    { key: "2", label: "About", path: "/about" },
    { key: "3", label: "Mapa", path: "/mapa" },
	{ key: "4", label: "Anomálie v datech", path: "/anomaly" },
  ];
  const location = useLocation();
  const navigate = useNavigate();
  const [selectedKey, setSelectedKey] = useState(
    items.find((_item) => location.pathname.startsWith(_item.path)).key
  );



  useEffect(() => {
    setSelectedKey(
      items.find((_item) => location.pathname.startsWith(_item.path)).key
    );
  }, [location]);

  return (
    <Layout>
      {/* <Sider trigger={null} theme="light" collapsible collapsed={collapsed}>
        <div style={{ height: "64px" }} />
        <Menu
          selectedKeys={[selectedKey]}
          style={{ height: "100%" }}
          mode="inline"
          onClick={onClickMenu}
        >
          {items.map((item) => (
            <Menu.Item key={item.key}>{item.label}</Menu.Item>
          ))}
        </Menu>
      </Sider> */}
      <Layout>
        {/* <Header style={{ padding: 0, background: colorBgContainer }}>
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            style={{
              fontSize: "16px",
              width: 64,
              height: 64,
            }}
          />
        </Header> */}
        <Content
          style={{
            margin: "24px 16px",
            padding: 24,
            minHeight: 280,
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
          }}
        >
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MyLayout;
