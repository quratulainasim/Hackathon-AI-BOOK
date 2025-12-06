import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
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
