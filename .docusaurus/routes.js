import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/docs',
    component: ComponentCreator('/docs', '4e6'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '86c'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'e8c'),
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
                component: ComponentCreator('/docs/capstone-overview/', '52e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/digital-twin-sim/',
                component: ComponentCreator('/docs/digital-twin-sim/', 'eed'),
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
                component: ComponentCreator('/docs/nvidia-isaac/', '5e1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ros2-fundamentals/',
                component: ComponentCreator('/docs/ros2-fundamentals/', 'b1a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-humanoids/',
                component: ComponentCreator('/docs/vla-humanoids/', 'da6'),
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
