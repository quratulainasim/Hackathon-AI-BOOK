import React from 'react';
import Layout from '@theme-original/Layout';
import ChatbotWidget from '@site/frontend/src/components/ChatbotWidget';

export default function LayoutWrapper(props) {
  return (
    <>
      <Layout {...props} />
      <ChatbotWidget />
    </>
  );
}
