import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', 'd1d'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '07e'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a99'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', '7ae'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '133'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', 'a3d'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '532'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'ca3'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '44c'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '52b'),
            routes: [
              {
                path: '/docs/appendices/glossary',
                component: ComponentCreator('/docs/appendices/glossary', 'aed'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/appendices/references',
                component: ComponentCreator('/docs/appendices/references', '8d4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/capstone-overview/',
                component: ComponentCreator('/docs/capstone-overview/', '779'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/digital-twin-sim/digital-twin-simulation',
                component: ComponentCreator('/docs/digital-twin-sim/digital-twin-simulation', '342'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/introduction/humanoid-architecture',
                component: ComponentCreator('/docs/introduction/humanoid-architecture', '6c0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/introduction/physical-ai',
                component: ComponentCreator('/docs/introduction/physical-ai', '0ae'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/nvidia-isaac/',
                component: ComponentCreator('/docs/nvidia-isaac/', 'ff5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ros2-fundamentals/',
                component: ComponentCreator('/docs/ros2-fundamentals/', 'f5e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-humanoids/vision-language-action',
                component: ComponentCreator('/docs/vla-humanoids/vision-language-action', '1d7'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '72e'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
